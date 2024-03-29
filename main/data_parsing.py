import json

from DataAccess import DBA, DAO
from Config import Config
from Plots import DisplayPlot

conf = Config.Config().get_config()


def get_actual_device_values(device_id, io_type='all'):
    """
    Get actual values of device (newest record from database) and prepare for device detail card
    :param device_id: device ID
    :param io_type: select in/out type of ability, default 'all' select both 'in' and 'out'
    :return: JSON object with actual values, description, unit, ...
    """
    db = DBA.Dba(conf.get('db', 'path'))
    device = db.get_device(device_id)

    device_values = []
    if device:
        try:
            abilities = json.loads(device.provided_func)
        except json.JSONDecodeError as e:
            print(conf.get('msg', 'decode_error'))
            abilities = []

        for ability in abilities:
            # get newest record from db
            records = db.get_record_from_device(device_id, value_type=ability['name'], limit=1)

            # select type of ability
            if ability['io'] == io_type or io_type == 'all':
                # select first item from record list or create empty dictionary if record list is empty
                if len(records) > 0:
                    record_dict = records[0].__dict__
                    record_dict['time'] = records[0].time
                else:
                    record_dict = {}

                record_dict['value_type'] = ability['user_name']
                record_dict['unit'] = ability['unit']
                record_dict['category'] = ability['category']
                record_dict['io'] = ability['io']
                record_dict['desc'] = ability['desc']
                record_dict['user_name'] = ability['user_name']
                record_dict['name'] = ability['name']
                device_values.append(record_dict)

    return device_values


def get_records_for_charts(device_id, value_type, from_date, to_date):
    """
    Get record from database for plot and charts
    :param device_id: device ID
    :param value_type: name of ability
    :param from_date: start of time interval
    :param to_date: end of time interval
    :return: JSON object of time labels and values
    """
    # TODO move this logic to DB layer
    db = DBA.Dba(conf.get('db', 'path'))
    records = db.get_record_from_device(device_id, value_type, limit=conf.getint('db', 'default_records_limit'))
    # TODO implement time interval from date - to date
    values = [float(record.value) for record in records]
    values.reverse()

    response = {
        # convert datetime objects to isoformat strings in reverse order
        'labels': list(reversed([record.time.isoformat() for record in records])),
        'values': values,
    }

    return response


def get_all_input_abilities():
    """
    Prepare input abilities for display setting
    :return: JSON list of devices witch provide input abilities and input abilities
    """
    db = DBA.Dba(conf.get('db', 'path'))
    records = db.get_devices()
    output = []
    for record in records:
        abilities = json.loads(record.provided_func)
        output_record = {'name': record.name, 'id': record.id}
        abilities_list = []
        for ability in abilities:
            if ability['io'] == 'in':
                abilities_list.append(ability)

        if len(abilities_list) != 0:
            output_record['abilities'] = abilities_list
            output.append(output_record)

    return output


def render_plot_64base_preview(device_id, ability):
    plot_data = get_records_for_charts(device_id, ability, 0, 0)
    plot = DisplayPlot.DisplayPlot(plot_data['values'], x_label_rotation=90)

    return plot.render_to_base64(width=320, height=240)


def get_screen_list(device_id, ability_name):
    db = DBA.Dba(conf.get('db', 'path'))
    screens = db.get_display(device_id, ability_name)

    for screen in screens:
        screen.params = json.loads(screen.params)  # parse screen setting like source device and ability
        source_device = db.get_device(
            screen.params.get('source_device'))  # load device to determine user names of device and ability

        screen.params['source_device_name'] = source_device.name

        # extract ability user name from provided_function JSON
        source_device_abilities = json.loads(source_device.provided_func)
        for ability in source_device_abilities:
            if ability.get('name') == screen.params.get('source_ability'):
                screen.params['source_ability_name'] = ability.get('user_name')

        screen.params['base64_plot'] = render_plot_64base_preview(screen.params.get('source_device'),
                                                                  screen.params.get('source_ability'))
    return screens
