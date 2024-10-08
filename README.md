# HospitalManagementAWS

This project will re-create the project found in my HospitalManagement repository but in aws.<br>
See original project link <a href="https://github.com/justirack/HospitalManagement">here</a> <br>
The project will have a front-end written in react and a backend that will use API gateway as its entry point and will be backed by lambda functions. Data will be stored in DynamoDB. 

# Tentative Architecture
The following draw.io diagram contains the tentative architecture diagram. The diagram will be updated to include appointments once users are complete.

![Alt](images/hospital_manager_diagram.svg)


# Endpoint Request Specifications
## user/add
The add user endpoint expects the following:
- First name
- Last name
- Date of birth (yyyy-mm-dd)
- Phone number (xxx)xxx-xxxx
- User type (patient or doctor)

Sample JSON:
```json
{
 "first_name": "Justin",
 "last_name": "Rackley",
 "date_of_birth": "2002-02-09",
 "phone_number": "(123)456-7890",
 "user_type": "patient|doctor"
}
```
The endpoint returns:
- A 200 status code if the user is successfully added to the database.
- A 400 status code if one or more parts of the request are invalid/improperly formatted.
- A 500 status code if something goes wrong with AWS.

## user/get
The get user endpoint expects the user id as a string query parameter. <br>
Sample input:
```text
id="12345678-1234-1234-123456789012"
```
The get endpoint returns:
- A 200 status code and the user(s) information if the id is valid.
- A 400 status code if the id that is passed is not valid.
- A 500 status code if something goes wrong with AWS.

## user/update
The update user endpoint expects a user ID and any **subset** of the following, and only the received values will be updated:
- First name
- Last name
- Date of birth (yyyy-mm-dd)
- Phone number (xxx)xxx-xxxx

Sample JSON:
```json
{
 "user_id": "12345678-1234-1234-123456789012",
 "first_name": "John",
 "last_name": "Thompson",
 "date_of_birth": "2003-01-19",
 "phone_number": "(987)654-3210"
}

```
The update endpoint returns:
- A 200 status code if the user's information is successfully updated in the database.
- A 400 status code if one or more parts of the request are invalid/improperly formatted.
- A 500 status code if something goes wrong with AWS.

## user/delete
The delete user endpoint expects a user ID in the body of the request, and will delete the user with that ID from the database.<be>
Sample JSON:
```json
{
    "user_id": "12345678-1234-1234-123456789012"
}
```
The delete endpoint returns:
- A 200 status code if the user's information is successfully deleted from the database.
- A 400 status code if a user ID is not passed, or something else is wrong with the request.
- A 500 status code if something goes wrong with AWS.




