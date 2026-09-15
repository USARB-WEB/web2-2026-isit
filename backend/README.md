# learning-backend

Learning-oriented FastAPI backend starter.

## Authentication

Email + password registration and login, issuing a JWT bearer token.

| Method | Endpoint               | Auth | Description                                   |
| ------ | ---------------------- | ---- | --------------------------------------------- |
| POST   | `/api/v1/auth/register`| no   | Create an account, returns a token (201)      |
| POST   | `/api/v1/auth/login`   | no   | Exchange credentials for a token              |
| GET    | `/api/v1/auth/me`      | yes  | The authenticated user's profile              |

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email": "ana@example.com", "password": "secret-password"}'
```

Send the returned token as `Authorization: Bearer <access_token>`.

### Protecting an endpoint

Depend on `get_current_user_id`, which validates the token and returns the
caller's user id:

```python
from fastapi import Depends

from app.api.v1.dependencies.auth import get_current_user_id


@router.get("/orders/mine")
def list_my_orders(user_id: int = Depends(get_current_user_id)):
    ...
```

### Notes

- Passwords are stored as salted bcrypt hashes; the plaintext never leaves
  the service layer and is never returned by the API.
- Login answers an unknown email and a wrong password identically, so the
  endpoint can't be used to enumerate registered accounts.
- `JWT_SECRET_KEY` in `.env` is a development placeholder — set a real
  random secret in any deployed environment. Rotating it invalidates all
  issued tokens.
