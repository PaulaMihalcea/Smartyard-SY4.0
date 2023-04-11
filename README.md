# Smartyard - SY4.0
# A wireless IoT system for environmental variables sensing, remote data storage and visualization
## Author: Paula Mihalcea
### Supervisors: Prof. Andrew David Bagdanov _([Università degli Studi di Firenze](https://www.unifi.it/))_, Walter Nunziati _([Magenta s.r.l.](https://www.magentalab.it/?lang=en))_
#### Università degli Studi di Firenze

---

![](https://img.shields.io/github/repo-size/paulamihalcea/Smartyard-SY4.0)

This project has been created as a **Computer Engineering thesis** at [Università degli Studi di Firenze](https://www.unifi.it/), in collaboration with [Magenta s.r.l.](https://www.magentalab.it/?lang=en) It represents a prototype for an **IoT system** that:

- retrieves generic **raw ambient data** from the sensors of one (or many) **TI SimpleLink SensorTag** device(s),
- **sends** it to a Raspberry Pi (or any other Linux device) using the Bluetooth Low Energy (BLE) protocol,
- **processes** it into a human-readable format,
- **stores** said data in an **Elasticsearch** database, and finally
- enables its graphical **visualization** using **Kibana**.

The complete code of the project is hereby provided as is, and is fully documented in the [`thesis.pdf`](thesis.pdf) file (in the Italian language) along with the detailed hardware configuration and requirements of the system.

  <p align="center">
    <img src="https://github.com/PaulaMihalcea/Smartyard-SY4.0/blob/master/architecture.png" width="80%" height="80%">
    <br>
    <sub>Architecture diagram.</sub>
  </p>
