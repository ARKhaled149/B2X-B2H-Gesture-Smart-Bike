# Smart Bike B2X Communication System

## Overview

This repository contains the code and documentation for the Smart Bike B2X (Bike-to-Everything) communication system. This project was developed as part of a Bachelor Thesis at the Media Engineering and Technology Faculty, German University in Cairo. It focuses on enhancing urban mobility by integrating smart bikes into the Internet of Things (IoT) ecosystem, enabling reliable and real-time communication between bikes and their surrounding environment.

## Thesis Summary

The Smart Bike B2X project addresses reducing human errors in urban transportation by developing a communication system that connects smart bikes with nearby infrastructures and other vehicles. The system is divided into two main components: the linking system and the calling system. The linking system utilizes socket programming to establish a secure and dependable connection between the bike and its environment, while the calling system employs gesture recognition to control the bike.

## Key Features

- **Server/Client Architecture**: Utilizes socket programming in Python to establish a robust server/client connection, allowing for real-time data exchange between the bike and other entities.
- **GPS Integration**: Incorporates a GPS module to provide accurate location and speed data, facilitating navigation and communication.
- **OLED Display**: Features an OLED screen for visual feedback, including QR code generation for security purposes.
- **Gesture Control**: Implements a gesture recognition system using machine learning to enable hands-free bike control.
- **Automatic Wi-Fi Connection**: Automatically connects to available networks, ensuring continuous communication without manual intervention.
- **Integration Server**: A cloud-based server that aggregates data from various bike systems, providing a centralized platform for data management and retrieval.

## Methodology

The project employs a combination of hardware components, including a Raspberry Pi 4, GPS module, OLED screen, and a mono camera, to create a comprehensive B2X communication system. The software architecture is built on Python, leveraging libraries for socket programming, machine learning, and data visualization.

## Results

The system was tested extensively, demonstrating reliable performance in establishing connections, exchanging data, and responding to gesture commands. Latency measurements indicate efficient operation, with the server and client components exhibiting minimal delay.

## Future Work

Future enhancements could include improved security measures, integration of face recognition for user authentication, and the development of autonomous navigation capabilities. Additionally, expanding the system to support larger data transfers and optimizing latency will further enhance its applicability in smart city environments.

## Conclusion

The Smart Bike B2X project successfully demonstrates the potential of integrating smart bikes into the IoT ecosystem, offering a scalable solution for enhancing urban mobility and reducing transportation-related human errors.

## Acknowledgments

I would like to thank and express my deep gratitude and appreciation to my thesis supervisor Assoc. Prof. Hassan Soubra for providing me with encouragement and enthusiasm, as well as his guidance and support throughout the project. I would also like to thank Mohammad Ihab, Mostafa El Hayani, Lydia Nabil, Abdelrahman Abozeid, my family, and friends for their continuous support and good company.
