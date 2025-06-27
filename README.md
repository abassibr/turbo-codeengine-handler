## 🧾 Turbonomic Action Group Routing Service
### 📌 Overview

This Flask-based application provides a serverless integration layer between **Turbonomic** and **ServiceNow**, hosted on **IBM Cloud Code Engine**. It ensures that only **approved actions** are sent to ServiceNow by programmatically managing Turbonomic group memberships.

It supports two key functions:

* Moving entities from a *pre-approved* group to an *approved* group (once a user approves the action).
* Restoring entities back to the *pre-approved* group (typically after an action has executed).

---

### ⚙️ Features

* ✅ Secure login to the Turbonomic API
* ✅ Group membership management via REST APIs
* ✅ Lightweight Flask app deployable to serverless platforms like Code Engine
* ✅ Logging and error handling for maintainability
* ✅ JSON-based webhook support

---

### 🚀 Endpoints

#### `POST /update_entity_group`

Used **after an action is approved** to:

* Remove the entity from the *pre-approved* group
* Add it to the *approved* group

**Request Body:**

```json
{
  "entity_uuid": "string"
}
```

#### `POST /restore_entity_group`

Used **after the action is executed** to:

* Remove the entity from the *approved* group
* Restore it back to the *pre-approved* group

**Request Body:**

```json
{
  "entity_uuid": "string"
}
```

---

### 🔐 Required Environment Variables

| Variable Name           | Description                                                             |
| ----------------------- | ----------------------------------------------------------------------- |
| `TURBOHOST`             | Base URL for the Turbonomic instance (e.g. `https://<your-turbo-host>`) |
| `TURBOUSER`             | Username for authenticating to the Turbonomic API                       |
| `TURBOPASS`             | Password for the Turbonomic user                                        |
| `PRE_APPROVED_GROUP_ID` | UUID of the group representing pending approvals                        |
| `APPROVED_GROUP_ID`     | UUID of the group representing approved entities                        |

---

### 🏗️ Deployment Notes

This app is designed to run as a containerized workload, ideally in a serverless environment like **IBM Cloud Code Engine**. You can build and deploy it using Docker or Podman and bind the environment variables via a `.env` file or service bindings.

**To run locally:**

```bash
export TURBOHOST=https://<your-turbo-url>
export TURBOUSER=<your-user>
export TURBOPASS=<your-pass>
export PRE_APPROVED_GROUP_ID=<uuid>
export APPROVED_GROUP_ID=<uuid>

python app.py
```

---

### 📄 Example Use Case

This service is typically invoked by a Turbonomic workflow **after an action is manually approved**, allowing an automation pipeline to:

* Maintain human oversight
* Filter low-value actions
* Improve compliance and change control by only forwarding approved actions to downstream systems like **ServiceNow**.

---
