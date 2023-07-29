import React, {useState} from 'react';

async function createUser(payload) {
    const url = "https://so354ite3h.execute-api.us-west-2.amazonaws.com/user/v1/user/add"

    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
        .then(response => response.json())
}

export default function CreateUserForm() {
    const [firstName, setFirstName] = useState();
    const [lastName, setLastName] = useState();

    const handleSubmit = async e => {
        e.preventDefault();
        const response = await createUser({
                "first_name": firstName,
                "last_name": lastName,
                "date_of_birth": "2002-02-09",
                "phone_number": "(123)456-7890",
                "user_type": "patient"

        })
    }

    return(
        <div className="create-user-wrapper">
            <h1>Please enter user information.</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    <p>First Name</p>
                    <input type="text" onChange={e => setFirstName(e.target.value)}/>
                </label>
                <label>
                    <p>Last Name</p>
                    <input type="text" onChange={e => setLastName(e.target.value)}/>
                </label>
                <div>
                    <button type="submit">Submit</button>
                </div>
            </form>
        </div>
    )
}
