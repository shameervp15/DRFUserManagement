# DRFUserManagement

---

# DRF + Vue User Management

A basic user management system built using Django REST Framework (backend) and Vue.js (frontend).
Functionality: Basic Profile Management and Notes Management
---

## Features

* User registration
* User login / authentication (token-based)
* Retrieve/update user profile
* Frontend in Vue.js consumes the DRF API

---

## Repository Structure

You will have two parts:

* `DRFUserManagement` — Django REST Framework backend
* `DRFUserManagementVue` — Vue.js frontend

---

## Prerequisites

Make sure you have installed:

* Python
* Node.js & npm (for Vue frontend)

---

## Setup Instructions

Below are step-by-step instructions to run the project locally.

### Backend (DRFUserManagement)

1. Clone or navigate to the backend repo:

   ```bash
   git clone https://github.com/shameervp15/DRFUserManagement.git
   cd DRFUserManagement
   ```

2. Create a virtual environment and activate it (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. (Optional) Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

   The API should now be running, e.g. at `http://127.0.0.1:8000/`

---

### Frontend (DRFUserManagementVue)

1. In a separate terminal, clone or move into the frontend directory:

   ```bash
   git clone https://github.com/shameervp15/DRFUserManagementVue.git
   cd DRFUserManagementVue
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. (Optional) If using vue CLI, you might have to ensure `vue` is installed or use `npx`:

   ```bash
   npm install -g @vue/cli
   ```

4. In the frontend code, check the API base URL (e.g. in an `axios` config) and point it to your backend (e.g. `http://127.0.0.1:8000/`).

5. Run the Vue development server:

   ```bash
   npm run serve
   ```

   The frontend should be accessible at something like `http://localhost:8080/`

---

## Usage

* Visit the frontend URL in your browser.
* Use the forms to register or login.
* The Vue app will make API calls to the DRF backend for user-related operations.
* You can also use tools like Postman or curl to test the REST endpoints directly.

---

## Tips & Notes

* Make sure CORS is configured in Django if frontend and backend run on different hosts/ports.
* Use environment variables or config files to store sensitive settings (secret key, DB credentials, etc.).
---
