# BangBang Termo

Un `climate` personalizado para controlar termos eléctricos con lógica bang-bang.

## Configuración en configuration.yaml

```yaml
climate:
  - platform: bangbang_termo
    name: Termo Solar
    temp_sensor: sensor.temperatura_termo
    switch: switch.termo
    min_temp: 40
    max_temp: 50
