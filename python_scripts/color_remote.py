entity_id = data.get('entity_id')
command = data.get('command')
logger.info("entity '{}' command '{}'".format(entity_id, command))

states = hass.states.get(entity_id)
brightness = states.attributes.get('brightness') or 0
off = brightness == 0
hsColor = states.attributes.get('hs_color') or [0,0]
hue = hsColor[0] or 0
sat = hsColor[1] or 0


logger.info("OLD Brightness {} Hue {} Sat {}".format(brightness, hue, sat))

if command == 'brightness':
  if off:
    hue = 0
    sat = 0.392
    brightness = 85
  elif brightness <= 168:
    brightness = 170
  elif brightness <= 250:
    brightness = 255
  else:
    brightness = 85


elif command == 'hue':
  suggested = hue + 30
  if suggested < 360:
    hue = suggested
  else:
    hue = 0

  if off:
    hue = 0
    sat = 33
    brightness = 85

  if sat < 1:
    sat = 33

elif command == 'sat':
  suggested = sat + 33
  if suggested < 100:
    sat = suggested
  else:
    sat = 33

  if off:
    hue = 0
    sat = 33
    brightness = 85


elif command == 'off':
  brightness = 0
  hue = 0
  sat = 0.392

else:
  logger.error("Invalid command: '{}".format(command))


logger.info("NEW Brightness {} Hue {} Sat {}".format(brightness, hue, sat))
service_data = {'entity_id': entity_id, 'hs_color': [hue, sat], 'brightness': brightness, 'transition': 0.1 }
hass.services.call('light', 'turn_on', service_data, False)

