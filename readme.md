# Aesir Bread Van App CLI Reference

This document provides a comprehensive guide to the Command Line Interface (CLI) commands available in the Aesir Bread Van application. These commands are defined in `wsgi.py` and can be executed using the Flask CLI.

## Prerequisites

Ensure you have your virtual environment activated and the dependencies installed.

```
pip install -r requirements.txt
```

## Global Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `init` | Creates and initializes the database. | `flask init` |

## User Commands (`user`)

Group for user management commands.

| Command | Description | Arguments | Usage |
|---------|-------------|-----------|-------|
| `create` | Creates a new user. | `username` (default: rob), `password` (default: robpass) | `flask user create <username> <password>` |
| `list` | Lists all users. | `format` (default: string, options: string, json) | `flask user list [format]` |

## Admin Commands (`admin`)

Group for administrative tasks, including managing drivers, residents, areas, and streets.

### Creation

| Command           | Description                      | Arguments                                                                           | Usage                                                                                        |
| ----------------- | -------------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `create-driver`   | Creates a new driver.            | `username`, `password`, `status` ('Off Duty'/'On Duty'), `area_name`, `street_name` | `flask admin create-driver <username> <password> <status> <area_name> <street_name>`         |
| `create-resident` | Creates a new resident.          | `username`, `password`, `area_name`, `street_name`, `house_number`                  | `flask admin create-resident <username> <password> <area_name> <street_name> <house_number>` |
| `create-area`     | Creates a new area.              | `name`                                                                              | `flask admin create-area <name>`                                                             |
| `create-street`   | Creates a new street in an area. | `name`, `area_name`                                                                 | `flask admin create-street <name> <area_name>`                                               |

### Listing

| Command | Description | Usage |
|---------|-------------|-------|
| `list-drivers` | Lists all drivers. | `flask admin list-drivers [format]` |
| `list-residents` | Lists all residents. | `flask admin list-residents [format]` |
| `list-areas` | Lists all areas. | `flask admin list-areas [format]` |
| `list-streets` | Lists all streets. | `flask admin list-streets [format]` |

### Updates

| Command         | Description            | Arguments               | Usage                                              |
| --------------- | ---------------------- | ----------------------- | -------------------------------------------------- |
| `update-street` | Updates a street name. | `street_id`, `new_name` | `flask admin update-street <street_id> <new_name>` |
| `update-area`   | Updates an area name.  | `area_id`, `new_name`   | `flask admin update-area <area_id> <new_name>`     |

### Deletion

| Command | Description | Arguments | Usage |
|---------|-------------|-----------|-------|
| `delete-driver` | Deletes a driver. | `driver_id` | `flask admin delete-driver <id>` |
| `delete-resident` | Deletes a resident. | `resident_id` | `flask admin delete-resident <id>` |
| `delete-area` | Deletes an area. | `area_id` | `flask admin delete-area <id>` |
| `delete-street` | Deletes a street. | `street_id` | `flask admin delete-street <id>` |

## Driver Commands (`driver`)

Group for driver-specific operations and drive management.

### Drive Management

| Command          | Description                | Arguments                                                         | Usage                                                                                       |
| ---------------- | -------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `schedule-drive` | Schedules a new drive.     | `username`, `area`, `street`, `date`, `time`, `--item` (multiple) | `flask driver schedule-drive <driver_username> <area> <street> <date> <time> -i "Name:Qty"` |
| `view-drives`    | Views drives for a driver. | `driver_username`                                                 | `flask driver view-drives <driver_username>`                                                |
| `start-drive`    | Starts a scheduled drive.  | `driver_username`, `drive_id`                                     | `flask driver start-drive <driver_username> <drive_id>`                                     |
| `complete-drive` | Completes a drive.         | `driver_username`, `drive_id`                                     | `flask driver complete-drive <driver_username> <drive_id>`                                  |
| `cancel-drive`   | Cancels a drive.           | `driver_username`, `drive_id`                                     | `flask driver cancel-drive <driver_username> <drive_id>`                                    |

### Items & Requests

| Command              | Description                      | Arguments                                              | Usage                                                                        |
| -------------------- | -------------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------- |
| `view-stop-requests` | Views stop requests for a drive. | `driver_username`, `drive_id`                          | `flask driver view-stop-requests <driver_username> <drive_id>`               |
| `add-drive-item`     | Adds an item to a drive.         | `driver_username`, `drive_id`, `item_name`, `quantity` | `flask driver add-drive-item <driver_username> <drive_id> <item_name> <qty>` |
| `remove-drive-item`  | Removes an item from a drive.    | `driver_username`, `drive_id`, `item_name`             | `flask driver remove-drive-item <driver_username> <drive_id> <item_name>`    |
| `view-drive-items`   | Views items in a drive.          | `driver_username`, `drive_id`                          | `flask driver view-drive-items <driver_username> <drive_id>`                 |

### Profile Updates

| Command                     | Description                       | Arguments                                          | Usage                                                                                |
| --------------------------- | --------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `update-driver-status`      | Updates driver status.            | `driver_username`, `status` ('Off Duty'/'On Duty') | `flask driver update-driver-status <driver_username> <status>`                       |
| `update-username`           | Updates driver username.          | `driver_username`, `new_username`                  | `flask driver update-username <driver_username> <new_username>`                      |
| `update-driver-area-info`   | Updates driver's assigned area.   | `driver_username`, `area_name`                     | `flask driver update-driver-area-info <driver_username> <area_name>`                 |
| `update-driver-street-info` | Updates driver's assigned street. | `driver_username`, `street_name`, `area_name`      | `flask driver update-driver-street-info <driver_username> <street_name> <area_name>` |

## Resident Commands (`resident`)

Group for resident interactions.

### Stop Requests

| Command               | Description                   | Arguments                                  | Usage                                                              |
| --------------------- | ----------------------------- | ------------------------------------------ | ------------------------------------------------------------------ |
| `request-stop`        | Requests a bus/van stop.      | `resident_username`, `drive_id`, `message` | `flask resident request-stop <resident_username> <drive_id> <msg>` |
| `cancel-stop`         | Cancels a stop request.       | `resident_username`, `stop_id`             | `flask resident cancel-stop <resident_username> <stop_id>`         |
| `get-requested-stops` | Gets list of requested stops. | `resident_username`                        | `flask resident get-requested-stops <resident_username>            |

### Information & Updates

| Command                          | Description                  | Arguments                                               | Usage                                                                                      |
| -------------------------------- | ---------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `get-driver-status-and-location` | Gets status/loc of a driver. | `driver_username`                                       | `flask resident get-driver-status-and-location <driver_username>`                          |
| `update-resident-area-info`      | Updates resident's area.     | `resident_username`, `new_area_name`                    | `flask resident update-resident-area-info <resident_username> <area_name>`                 |
| `update-resident-street-info`    | Updates resident's street.   | `resident_username`, `new_street_name`, `new_area_name` | `flask resident update-resident-street-info <resident_username> <street_name> <area_name>` |
| `update-house-number`            | Updates house number.        | `resident_username`, `new_house_number`                 | `flask resident update-house-number <resident_username> <new_house_number>`                |

### Notifications & Subscriptions

| Command                   | Description                      | Arguments                                       | Usage                                                                                |
| ------------------------- | -------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------ |
| `get-notifications`       | Gets notification history.       | `resident_username`                             | `flask resident get-notifications <resident_username>`                               |
| `read-notification`       | Marks a notification as read.    | `resident_username`, `notification_id`          | `flask resident read-notification <resident_username> <notification_id>`             |
| `subscribe-to-street`     | Subscribes to street alerts.     | `resident_username`, `street_name`, `area_name` | `flask resident subscribe-to-street <resident_username> <street_name> <area_name>`   |
| `unsubscribe-from-street` | Unsubscribes from street alerts. | `resident_username`, `street_name`, `area_name` | `flask resident unsubscribe-to-street <resident_username> <street_name> <area_name>` |

## Item Commands (`item`)

Group for inventory item management.

| Command       | Description               | Arguments                                            | Usage                                                 |
| ------------- | ------------------------- | ---------------------------------------------------- | ----------------------------------------------------- |
| `create-item` | Creates a new item.       | `name`, `price`, `description`, `tags` (JSON string) | `flask item create-item <name> <price> <desc> <tags>` |
| `list-items`  | Lists all items.          | `format`                                             | `flask item list-items [format]`                      |
| `update-item` | Updates an existing item. | `item_id`, `[name]`, `[price]`, `[desc]`, `[tags]`   | `flask item update-item <id> [args]`                  |
| `delete-item` | Deletes an item.          | `item_id`                                            | `flask item delete-item <id>`                         |

## Test Commands (`test`)

Commands for running the test suite.

| Command | Description | Usage |
|---------|-------------|-------|
| `all` | Runs all tests. | `flask test all` |
| `unit` | Runs unit tests (App/tests/unit). | `flask test unit` |
| `int` | Runs integration tests (App/tests/integration). | `flask test int` |
