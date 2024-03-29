import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Device
from .data_parsing import *
from DataAccess import DBA, DAO
from DeviceCom import DataSender
from Config import Config
from Plots import DisplayPlot

# TODO handle 404 page not found error
# TODO maximalizovat predavani hodnot do templatu - snizit pocet leteraru v templatech

conf = Config.Config().get_config()
input_abilities = conf.get('db', 'input_abilities').split(',')
output_abilities = conf.get('db', 'output_abilities').split(',')


def index(request):
    """
    Main page with list of all devices
    :param request:
    :return: Main page
    """
    devices = Device.get_all()

    devices_id_lst = [device.id for device in devices]

    response = {'msg': 'Devices',
                'devices': devices,
                'devices_json': json.dumps(devices_id_lst),
                'time_to_live': 30,
                }
    return render(request, "main/index.html", response)


def device_detail(request, device_id):
    """
    Device detail page
    :param request:
    :param device_id: device ID
    :return: device detail page
    """
    db = DBA.Dba(conf.get('db', 'path'))
    device = db.get_device(device_id)
    # device = Device.get(device_id)
    records = db.get_record_from_device(device_id, limit=10)
    # records = Record.get_all(device_id, limit=10)

    actual_in_values = get_actual_device_values(device_id, io_type='in')
    actual_out_values = get_actual_device_values(device_id, io_type='out')
    print(actual_out_values)

    response = {'device': device,
                'values': records,
                'actual_values': actual_in_values,
                'actual_out_values': actual_out_values,
                'device_status_interval': 30000,  # status refresh interval in seconds
                'device_values_interval': 3000,  # values refresh interval in seconds
                }
    return render(request, 'main/device_detail.html', response)


def waiting_devices(request):
    """
    List of all waiting device
    :param request:
    :return: waiting device page
    """
    db = DBA.Dba(conf.get('db', 'path'))
    devices = db.get_waiting_devices()

    response = {'title': 'Waiting devices',
                'devices': devices,
                'input_abilities': input_abilities,
                'output_abilities': output_abilities,
                }
    return render(request, 'main/waiting_devices.html', response)


def display(request, ability_name, device_id):
    """
    Display setting page - allow sendig data to connected displays
    :param request:
    :param ability_name: name od display ability
    :param device_id: device ID
    :return: display setting page
    """
    # plot_data = get_records_for_charts('8394748', 'DS18B20', 0, 0)
    # print(plot_data)
    # plot = DisplayPlot.DisplayPlot(plot_data['values'], x_label_rotation=90)

    response = {
        'screens': get_screen_list(device_id, ability_name),  # list of screen settings
        'devices': get_all_input_abilities(),  # list of all devices and their input abilities
        'options': ['plot', 'text'],
        'ability_name': ability_name,
        'device_id': device_id,
        # 'plot': plot.render_to_base64(width=320, height=240),
    }

    return render(request, 'main/display.html', response)


""" FORMS """


def verify_device(request, device_id):
    db = DBA.Dba(conf.get('db', 'path'))
    device = db.get_waiting_device(device_id)  # get waiting device for transfer to permanent devices table
    db.remove_waiting_device(device_id)  # remove device from waiting devices table

    # if hidden remove input is set to false -> save new device to db
    if request.POST['remove-device'] == 'false':
        # sending MQTT message to device
        sender = DataSender.DataSender()
        sender.verify_device(device_id)

        abilities = []
        # get modified abilities from user form
        for ability in device.provided_func:
            io_type = 'in' if request.POST['category-' + ability] in input_abilities else 'out'
            abilities.append(DAO.Ability(name=ability,
                                         io=io_type,
                                         user_name=request.POST['user-name-' + ability],
                                         category=request.POST['category-' + ability],
                                         unit=request.POST['unit-' + ability],
                                         desc=request.POST['desc-' + ability],
                                         ))

        abilities_json = json.dumps([a.__dict__ for a in abilities])  # create json from abilities
        new_device = DAO.Device(device.id, request.POST['device-name'], abilities_json)

        db.insert_device(new_device)  # add new device to database

    return HttpResponseRedirect(reverse('main:waiting_devices'))


def remove_device(request, device_id):
    """
    Remove device from database
    :param request: 
    :param device_id: device ID
    :return: redirect to home page
    """
    db = DBA.Dba(conf.get('db', 'path'))
    if request.POST['remove-device'] == 'true':
        print('true')
        db.remove_device(device_id)

    return HttpResponseRedirect(reverse('main:index'))


def output_action(request, device_id, ability):
    """
    Provide output action to devices. Convert UI events (button click, switch switch, ...) to MQTT messages.
    :param request:
    :param device_id: device ID
    :param ability: name of output ability
    :return: simple 'ok' message
    """
    if request.is_ajax() and request.POST['device'] == device_id:
        sender = DataSender.DataSender()
        sender.send_data_to_device(request.POST['device'], request.POST['ability'], request.POST['state'])
        # sender.verify_device(device_id)
        print('sending', request.POST['device'], request.POST['ability'], request.POST['state'])

    return HttpResponse('ok')


def save_screen(request, device_id):
    """
    Receive screen parameters from display setting. Insert or update existing screen from DB. Action for 'add screen' and 'save' btn. 
    :param request: 
    :param device_id: parent device ID
    :return: 
    """
    if request.is_ajax() and request.POST.get('destination-device') == device_id and request.POST.get(
            'destination-display-name'):

        screen_id = request.POST.get('destination-screen-id')
        screen_params = {'source_device': request.POST.get('data-source-device'),
                         'source_ability': request.POST.get('data-source-ability')}

        db = DBA.Dba(conf.get('db', 'path'))
        if screen_id:
            # update display setting (already have screen_id)
            old_display = db.get_screen(screen_id)
            old_display.params = json.dumps(screen_params)
            db.update_display(old_display)

        else:
            # insert new display settings (dont have screen_id)
            new_display = DAO.Display(device_id=request.POST.get('destination-device'),
                                      display_name=request.POST.get('destination-display-name'),
                                      params=json.dumps(screen_params))
            db.insert_display(new_display)

    return HttpResponse('ok')


""" APIs """


def waiting_devices_api(request):
    """
    Provide data about waiting devices
    :param request:
    :return: JSON list of all waiting devices
    """
    db = DBA.Dba(conf.get('db', 'path'))
    devices = db.get_waiting_devices()

    response = json.dumps([device.__dict__ for device in devices])
    return HttpResponse(response)


def telemetry_api(request, device_id):
    """
    Provide actual telemetry data
    :param request:
    :param device_id: device ID
    :return: JSON last telemetry record from DB
    """
    db = DBA.Dba(conf.get('db', 'path'))
    telemetry = db.get_telemetry(device_id)

    if telemetry:
        response = json.dumps(telemetry.__dict__)
        return HttpResponse(response)
    else:
        return HttpResponse('{}')


def device_actual_values_api(request, device_id):
    """
    Provide actual device values
    :param request:
    :param device_id: device ID
    :return: JSON last values records from DB
    """
    device_values = get_actual_device_values(device_id)

    # handle not serializable datetime objects in device_values
    for value in device_values:
        value['time'] = value['time'].isoformat() if 'time' in value else None

    return HttpResponse(json.dumps(device_values))


def records_api(request, device_id, ability):
    """
    Provide data for JS chart library
    :param request:
    :param device_id: device ID
    :param ability: name of ability
    :return: JSON with chart parameters and plot data with values and time lables
    """
    response = get_records_for_charts(device_id, ability, 0, 0)

    # convert datetime object to isoformat string
    response['chart_type'] = 'line'
    response['data_type'] = ability
    response['data_label'] = ability
    response['border_color'] = "#1e88e5"
    response['is_filled'] = 'false'

    return HttpResponse(json.dumps(response))


def display_preview_api(request, device_id, ability):
    """
    Render Base64 plot preview for display setting page
    :param request:
    :param device_id: device ID
    :param ability: ability name
    :return: base64 uri with plot preview
    """

    return HttpResponse(render_plot_64base_preview(device_id, ability))
