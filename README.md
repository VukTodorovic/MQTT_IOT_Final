# MQTT_IOT_Final
Mock implementation of IOT security system written in Python using MQTT and SSDP protocols

## System Sketch
![image](https://github.com/VukTodorovic/MQTT_IOT_Final/assets/77984795/35e0e643-1416-4d6c-a80f-6b26e9ee3be4)

## Workflow
- System consists of MQTT broker server, 2 smart sensor devices and 1 smart actuator device
- Broker serves uses SSDP implementation to send M_SEARCH beacons every few seconds
- Other smart devices listen on broadcast ip and when the beacon arives they respons with NOTIFY message so that broker know which devices are connecting to it
- After sending NOTIFY message, smart devices connect to the MQTT broker since now they now its IP address and they start subscribing or publishing to the MQTT topics on the broker

## Door Lock
- Used for authorization of the access to the secured object
- They mock the usage of sensors for reading the persons ID card and also its height and weight to verify that the ID card wasn't stolen
- Device combines those 3 sensors to reliably identify the person
- Every time someone tries to go in the protected object, Door Lock device will publish the success or failure of going in to the topic "topic/door"

## Pressure Table
- In the protected object there are protected goods sitting on a table
- This device is mock implementation of the table that measures pressure and thereby measure the weight of the protected goods
- Every few seconds, this device will publish the current weight of the object to the topic "topic/pressure"

## Alarm
- This device is a mock implementation of an actuator device that turns on an alaram whenever there is a security issue
- It subscribes to the both "topic/door" and "topic/pressure" topics
- If the message comes from the "topic/door" it checks if the json object "success" equals to the "success" value and if it doesn't, the alarm will start
- IF the message comes from the "topic/pressure" it checks if the pressure value is equal to the expected weight of the protected goods on the table and if it isn't, the alarm will start

## Broker
- Acts as a controller in the system and is responsible for being the central middleman of the MQTT conversation
- Also on the broker there is available info on data of all topics
