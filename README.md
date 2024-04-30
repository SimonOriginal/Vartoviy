# Vartoviy

[Read in Russian](./README_RU.md) [Read in Ukrainian](./README_UA.md)

**Vartoviy** (working title - "Вартовий") is an open-source platform specially designed for creating custom animal monitoring infrastructure on farms where they roam in open spaces. With Vartoviy, you can easily deploy a server in a Docker container or on your own computer, ensuring a high level of privacy and full control over your data. This project provides full transparency with open access to the server source code, device firmware, and detailed device schematics, allowing users to fully understand its operation.

**Please note that "Vartoviy" is currently in development.**

### Screenshots
<p align="center">
    <img src="https://github.com/SimonOriginal/Guardian/assets/94782611/0c8d4f81-c148-4550-9c5f-162a96852ee7" width="320" alt="Image 1">
    <img src="https://github.com/SimonOriginal/Guardian/assets/94782611/bfeffd59-6495-4e8a-aae7-6002a8e28272" width="320" alt="Image 2">
    <img src="https://github.com/SimonOriginal/Guardian/assets/94782611/04bb9161-e431-4744-9a70-8b552df96e54" width="320" alt="Image 3">
    <img src="https://github.com/SimonOriginal/Guardian/assets/94782611/1b368e06-d0d2-4cc2-9e98-297028a426f7" width="320" alt="Image 4">
    <img src="https://github.com/SimonOriginal/Guardian/assets/94782611/a0e8a050-f1ba-44c3-bdc0-9c12a319c9ce" width="320" alt="Image 5">
    <img src="https://github.com/SimonOriginal/Guardian/assets/94782611/06751e6d-1d3b-4d44-baec-b897ca2574ba" width="320" alt="Image 6">
    <img src="https://github.com/SimonOriginal/Guardian/assets/94782611/be24ec32-cc9d-4b63-9b98-a7f5e1387a03" width="320" alt="Image 7">
    <img src="https://github.com/SimonOriginal/Guardian/assets/94782611/b0bd8b6b-1bbe-4910-b537-fdb11c96e33c" width="320" alt="Image 8">
</p>

### Features
* **Localization for Different Languages:** Users can select the interface language from options including "🇬🇧 English," "🇺🇦 Ukrainian," and "🇷🇺 Russian."
* **Barrier Breach Notifications:** The system provides notifications in case of a specified barrier breach, ensuring prompt alerts about events.
* **Low Battery Notifications (20%):** Users receive notifications when the battery level on the device reaches 20%, providing timely warnings about the need for charging.
* **Theme Switching:** Users can switch between "🌞 Light" and "🌚 Dark" interface themes, providing a comfortable user experience in various lighting conditions.
* **Device Connection via MQTT:** MQTT protocol is used for stable and efficient device connections, ensuring reliable data transmission.
* **Display of Latest Data in Dashboard:** Users can visually track the latest device data through an intuitive and informative dashboard.
* **Viewing Full Movement History:** Provides the ability to view the full movement history of a specific device, allowing for deeper analysis of its activity.
* **Graphical Display and Modal Windows:** Graphical representation of data and the ability to analyze it in detail through modal windows provide a deeper understanding of information.
* **Creating and Saving Barriers for Specific Devices:** Users can define and save a barrier for a specific device, providing personalized and flexible control.
* **Display of Device Location and Barrier on Map:** Visual representation of the current device location and set barrier on the map.
* **Ability to Download GeoJson of Configured Barrier:** Users can easily download barrier geographic data in GeoJson format for further use or analysis.

### Installation Options
* **<u>Docker</u>**
* **<u>Alternative Installation</u>**

### Quick Start with Docker 🐳

To launch a project in a Docker container, follow these steps:

1. **Build a Docker image**:

   ```
   docker build -t vartoviy .
   ```

2. **Starting Docker container**:

   ```
   docker run -p 8000:8000 -d vartoviy
   ```

   This command will start the container in the background, assign port 8000 on your host to port 8000 in the container, and use the image name you specified earlier.

3. **Access the project**: You can now open the project in your browser at http://localhost:8000/.

### Variant with External PostgreSQL Database

Before running the build, you need to change the database bindings in the settings.py file.

1. **Building Docker Image**:

   ```bash
   docker-compose up -d
   ```

2. **Database Setup**:

   To set up the database and create a superuser with authentication data, follow these steps:

   ```bash
   docker-compose exec web sh -c "python manage.py makemigrations && python manage.py migrate" &&
   docker-compose down &&
   docker-compose up --build -d &&
   docker-compose exec -e DJANGO_SUPERUSER_USERNAME=admin -e DJANGO_SUPERUSER_EMAIL=admin@example.com -e DJANGO_SUPERUSER_PASSWORD=adminpassword web bash -c "python manage.py createsuperuser --noinput"
   ```

   These commands will update the database, restart Docker containers, and create a superuser with the username "admin," email "admin@example.com," and password "adminpassword" (please use more secure passwords in real applications).

🚀 Done! Now you have a Docker image with a configured database and superuser for your Django application.

### Alternative Installation 🚀

1. **Create a virtual environment**:

   ```
   python -m venv venv
   ```

2. **Activating the virtual environment**:

   ```
   .\venv\Scripts\Activate.ps1.
   ```

3. **Installing dependencies**:

   ```
   pip install -r "requirements.txt"
   ```

4. **Migrations**:

   ```
   python manage.py makemigrations
   ```

   ```
   python manage.py migrate
   ```

5. **Starting the server**:

   ```
   python manage.py runserver
   ```
You can now open the project in your browser at http://localhost:8000/.

6. **Start the script for virtual sensors (optional)**:

   ```
   python mqtt_virtual_sensor.py
   ```
