
# Honeygain Flask API

This project wraps the Honeygain API endpoints into a Flask server with well-defined routes.

## Features

- User registration and authentication
- Fetch user details, TOS status, balances, traffic stats
- List and manage devices
- List referrals and transactions
- Change password and device titles

## Requirements

- Python 3.7+
- `pip install -r requirements.txt`

## Installation

1. Clone the repository:
```bash
   git clone <repo_url>
   cd <project_folder>
````

2. Create a `.env` file under `Keys/keys.env`:

   ```dotenv
   HONEYGAIN_EMAIL=your_email@example.com
   HONEYGAIN_PASS=your_password
   ```
3. Install dependencies:

   ```bash
   pip install flask requests python-dotenv firebase-admin
   ```

## Usage

Start the Flask server:

```bash
python api.py
```

The server will run on `http://localhost:5000` by default.

## Endpoints

| Route                          | Method   | Description                                                |              |
| ------------------------------ | -------- | ---------------------------------------------------------- | ------------ |
| `/auth/register`               | POST     | Register a new user                                        |              |
| `/auth/token`                  | POST     | Obtain an access token                                     |              |
| `/users/me`                    | GET      | Get user profile (requires `Authorization` header)         |              |
| `/users/tos`                   | GET      | Get TOS status                                             |              |
| `/stats/traffic`               | GET      | Get traffic statistics                                     |              |
| `/users/balances`              | GET      | Get balances                                               |              |
| \`/devices?deleted=\[true      | false]\` | GET                                                        | List devices |
| `/referrals`                   | GET      | List referrals                                             |              |
| `/transactions`                | GET      | List transactions                                          |              |
| `/users/password`              | PUT      | Change password (JSON: `current_password`, `new_password`) |              |
| `/devices/<device_id>/title`   | PUT      | Change device title (JSON: `title`)                        |              |
| `/devices/<device_id>`         | DELETE   | Delete a device                                            |              |
| `/devices/<device_id>/restore` | PATCH    | Restore a deleted device                                   |              |

## License

MIT
