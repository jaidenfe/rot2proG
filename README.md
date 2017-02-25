<img src="https://i.imgur.com/ztkbg9I.png" alt="UBNL Logo" width="140" height="auto" align="right">
# rot2proG
>University at Buffalo Nanosatellite Laboratory 2016<br>
>Created By Jaiden Ferraccioli<br>
>E-mail: jaidenfe@buffalo.edu<br>
>Current Version: v1.0

This is a control interface for the SPID Elektronik rot2proG antenna rotor controller. Protocol documentation was adapted from http://ryeng.name/blog/3. The SPID protocol supports 3 commands: stop, status and set. The stop command stops the rotor in its current position and returns the aproximate position it has stopped in. The status command returns the current position of the rotor. The set command tells the rotor to rotate to a given position.

The rotor controller communicates with the PC using a serial connection. Communication parameters are 600 bps, 8 bits, no parity and 1 stop bit. In order for the computer to communicate with the rotor, the controller must be set to the "Auto" setting. This can be done by pressing the function key ("F") until you see an "A" displayed in the left-most screen on the controller.

All commands are issued as 13 byte packets, and responses are received as 12 byte packets.

===

<h3>Command Packet</h3>
<table>
  <tr>
    <td><b>Byte:</td>
    <td><b>0</td>
    <td><b>1</td>
    <td><b>2</td>
    <td><b>3</td>
    <td><b>4</td>
    <td><b>5</td>
    <td><b>6</td>
    <td><b>7</td>
    <td><b>8</td>
    <td><b>9</td>
    <td><b>10</td>
    <td><b>11</td>
    <td><b>12</td>
  </tr>
  <tr>
    <td><b>Fields:</td>
    <td>START</td>
    <td>H1</td>
    <td>H2</td>
    <td>H3</td>
    <td>H4</td>
    <td>PH</td>
    <td>V1</td>
    <td>V2</td>
    <td>V3</td>
    <td>V4</td>
    <td>PV</td>
    <td>K</td>
    <td>END</td>
  </tr>
  <tr>
    <td><b>Value:</td>
    <td>0x57</td>
    <td>0x3?</td>
    <td>0x3?</td>
    <td>0x3?</td>
    <td>0x3?</td>
    <td>0x0?</td>
    <td>0x3?</td>
    <td>0x3?</td>
    <td>0x3?</td>
    <td>0x3?</td>
    <td>0x0?</td>
    <td>0x?F</td>
    <td>0x20</td>
  </tr>
</table>

* <b>START</b> - Start byte (always 0x57)
* <b>H1 - H4</b> - Azimuth as ASCII characters 0-9
* <b>PH</b> - Azimuth resolution in pulses per degree (ignored in command packet)
* <b>V1 - V4</b> - Elevation as ASCII characters 0-9
* <b>PV</b> - Elevation resolution in pulses per degree (ignored in command packet)
* <b>K</b> - Command (0x0F = STOP | 0x1F = STATUS | 0x2F = SET)
* <b>END</b> - End byte (always 0x20)

===
<h3>Response Packet</h3>
<table>
  <tr>
    <td><b>Byte:</td>
    <td><b>0</td>
    <td><b>1</td>
    <td><b>2</td>
    <td><b>3</td>
    <td><b>4</td>
    <td><b>5</td>
    <td><b>6</td>
    <td><b>7</td>
    <td><b>8</td>
    <td><b>9</td>
    <td><b>10</td>
    <td><b>11</td>
  </tr>
  <tr>
    <td><b>Fields:</td>
    <td>START</td>
    <td>H1</td>
    <td>H2</td>
    <td>H3</td>
    <td>H4</td>
    <td>PH</td>
    <td>V1</td>
    <td>V2</td>
    <td>V3</td>
    <td>V4</td>
    <td>PV</td>
    <td>END</td>
  </tr>
  <tr>
    <td><b>Value:</td>
    <td>0x57</td>
    <td>0x0?</td>
    <td>0x0?</td>
    <td>0x0?</td>
    <td>0x0?</td>
    <td>0x0?</td>
    <td>0x0?</td>
    <td>0x0?</td>
    <td>0x0?</td>
    <td>0x0?</td>
    <td>0x0?</td>
    <td>0x20</td>
  </tr>
</table>

* <b>START</b> - Start byte (always 0x57)
* <b>H1 - H4</b> - Azimuth as byte values
* <b>PH</b> - Azimuth resolution in pulses per degree
* <b>V1 - V4</b> - Elevation as byte values
* <b>PV</b> - Elevation resolution in pulses per degree
* <b>END</b> - End byte (always 0x20)

Positions are decoded using the following formulas:

  _az = H1 * 100 + H2 * 10 + H3 + H4 / 10 - 360_ <br>
  _el = V1 * 100 + V2 * 10 + V3 + V4 / 10 - 360_

<h3>Degree Per Pulse</h3>
<table>
  <tr>
    <td><b>Deg/pulse</td>
    <td><b>PH</td>
    <td><b>PV</td>
  </tr>
  <tr>
    <td><b>1</td>
    <td>0x01</td>
    <td>0x01</td>
  </tr>
  <tr>
    <td><b>0.5</td>
    <td>0x02</td>
    <td>0x02</td>
  </tr>
  <tr>
    <td><b>0.20</td>
    <td>0x04</td>
    <td>0x04</td>
  </tr>
</table>

> NOTE: The PH and PV values in the response packet reflect the settings of the rotator controller. The Rot2Prog supports the following resolutions (always the same for azimuth and elevation):

===
<h3>Stop Command</h3>

_Command Packet_

<table>
  <tr>
    <td><b>Byte:</td>
    <td><b>0</td>
    <td><b>1</td>
    <td><b>2</td>
    <td><b>3</td>
    <td><b>4</td>
    <td><b>5</td>
    <td><b>6</td>
    <td><b>7</td>
    <td><b>8</td>
    <td><b>9</td>
    <td><b>10</td>
    <td><b>11</td>
    <td><b>12</tb>
  </tr>
  <tr>
    <td><b>Fields:</td>
    <td>START</td>
    <td>H1</td>
    <td>H2</td>
    <td>H3</td>
    <td>H4</td>
    <td>PH</td>
    <td>V1</td>
    <td>V2</td>
    <td>V3</td>
    <td>V4</td>
    <td>PV</td>
    <td>K</td>
    <td>END</td>
  </tr>
  <tr>
    <td><b>Value:</td>
    <td>0x57</td>
    <td>0x00</td>
    <td>0x00</td>
    <td>0x00</td>
    <td>0x00</td>
    <td>0x00</td>
    <td>0x00</td>
    <td>0x00</td>
    <td>0x00</td>
    <td>0x00</td>
    <td>0x00</td>
    <td>0x0F</td>
    <td>0x20</td>
  </tr>
</table>

<br>

_Response Packet Example_

<table>
  <tr>
    <td><b>Byte:</td>
    <td><b>0</td>
    <td><b>1</td>
    <td><b>2</td>
    <td><b>3</td>
    <td><b>4</td>
    <td><b>5</td>
    <td><b>6</td>
    <td><b>7</td>
    <td><b>8</td>
    <td><b>9</td>
    <td><b>10</td>
    <td><b>11</td>
  </tr>
  <tr>
    <td><b>Fields:</td>
    <td>START</td>
    <td>H1</td>
    <td>H2</td>
    <td>H3</td>
    <td>H4</td>
    <td>PH</td>
    <td>V1</td>
    <td>V2</td>
    <td>V3</td>
    <td>V4</td>
    <td>PV</td>
    <td>END</td>
  </tr>
  <tr>
    <td><b>Value:</td>
    <td>0x57</td>
    <td>0x03</td>
    <td>0x07</td>
    <td>0x02</td>
    <td>0x05</td>
    <td>0x02</td>
    <td>0x03</td>
    <td>0x09</td>
    <td>0x04</td>
    <td>0x00</td>
    <td>0x02</td>
    <td>0x20</td>
  </tr>
</table>

_az = 372.5 - 360 = 12.5_ <br>
_el = 394.0 - 360 = 34.0_ <br>
_PH = PV = 0x02 (pulse for each 0.5 deg)_

===
<h3>Status Command</h3>
The status command returns the current position of the antenna

_Command Packet_

<table>
  <tr>
    <td><b>Byte:</td>
    <td><b>0</td>
    <td><b>1</td>
    <td><b>2</td>
    <td><b>3</td>
    <td><b>4</td>
    <td><b>5</td>
    <td><b>6</td>
    <td><b>7</td>
    <td><b>8</td>
    <td><b>9</td>
    <td><b>10</td>
    <td><b>11</td>
    <td><b>12</tb>
  </tr>
  <tr>
    <td><b>Fields:</td>
    <td>START</td>
    <td>H1</td>
    <td>H2</td>
    <td>H3</td>
    <td>H4</td>
    <td>PH</td>
    <td>V1</td>
    <td>V2</td>
    <td>V3</td>
    <td>V4</td>
    <td>PV</td>
    <td>K</td>
    <td>END</td>
  </tr>
  <tr>
    <td><b>Value:</td>
    <td>0x57</td>
    <td>0x00</td>
    <td>0x00</td>
    <td>0x00</td>
    <td>0x00</td>
    <td>0x00</td>
    <td>0x00</td>
    <td>0x00</td>
    <td>0x00</td>
    <td>0x00</td>
    <td>0x00</td>
    <td>0x1F</td>
    <td>0x20</td>
  </tr>
</table>

<br>

_Response Packet Example_

<table>
  <tr>
    <td><b>Byte:</td>
    <td><b>0</td>
    <td><b>1</td>
    <td><b>2</td>
    <td><b>3</td>
    <td><b>4</td>
    <td><b>5</td>
    <td><b>6</td>
    <td><b>7</td>
    <td><b>8</td>
    <td><b>9</td>
    <td><b>10</td>
    <td><b>11</td>
  </tr>
  <tr>
    <td><b>Fields:</td>
    <td>START</td>
    <td>H1</td>
    <td>H2</td>
    <td>H3</td>
    <td>H4</td>
    <td>PH</td>
    <td>V1</td>
    <td>V2</td>
    <td>V3</td>
    <td>V4</td>
    <td>PV</td>
    <td>END</td>
  </tr>
  <tr>
    <td><b>Value:</td>
    <td>0x57</td>
    <td>0x03</td>
    <td>0x07</td>
    <td>0x02</td>
    <td>0x05</td>
    <td>0x02</td>
    <td>0x03</td>
    <td>0x09</td>
    <td>0x04</td>
    <td>0x00</td>
    <td>0x02</td>
    <td>0x20</td>
  </tr>
</table>

_az = 372.5 - 360 = 12.5_ <br>
_el = 394.0 - 360 = 34.0_ <br>
_PH = PV = 0x02 (pulse for each 0.5 deg)_

> NOTE: Status commands can be issued while the rotator is moving and will always return the current position

===
<h3>Set Command</h3>
The set command tells the rotator to turn to a specific position. The controller does not send a response to this command.

Azimuth and elevation is calculated as number of pulses, with a +360 degree offset (so that negative position can be encoded with positive numbers).

Rot2Prog supports different resolutions:

_H = PH * (360 + az)_ <br>
_V = PV * (360 + el)_

H1-H4 and V1-V4 are these numbers encoded as ASCII (0x30-0x39, i.e., '0'-'9').

<h5>Example</h5>
Pointing a Rot2Prog to azimuth 123.5, elevation 77.0 and a 0.5 degree per pulse value (PH=PV=2):

_H = 2 * (360 + 123.5) = 967_ <br>
_V = 2 * (360 + 77.0) = 874_

<table>
  <tr>
    <td><b>Byte:</td>
    <td><b>0</td>
    <td><b>1</td>
    <td><b>2</td>
    <td><b>3</td>
    <td><b>4</td>
    <td><b>5</td>
    <td><b>6</td>
    <td><b>7</td>
    <td><b>8</td>
    <td><b>9</td>
    <td><b>10</td>
    <td><b>11</td>
    <td><b>12</tb>
  </tr>
  <tr>
    <td><b>Fields:</td>
    <td>START</td>
    <td>H1</td>
    <td>H2</td>
    <td>H3</td>
    <td>H4</td>
    <td>PH</td>
    <td>V1</td>
    <td>V2</td>
    <td>V3</td>
    <td>V4</td>
    <td>PV</td>
    <td>K</td>
    <td>END</td>
  </tr>
  <tr>
    <td><b>Value:</td>
    <td>0x57</td>
    <td>0x30</td>
    <td>0x39</td>
    <td>0x36</td>
    <td>0x37</td>
    <td>0x02</td>
    <td>0x30</td>
    <td>0x38</td>
    <td>0x37</td>
    <td>0x34</td>
    <td>0x02</td>
    <td>0x2F</td>
    <td>0x20</td>
  </tr>
</table>

>NOTE: The PH and PV values sent are ignored. The values used by the rotator control unit are set by choosing resolution in the setup menu. These values can be read using the status command if they are not known.
