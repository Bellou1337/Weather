# FastAPI Database API

## API Endpoints

| Метод                          | Описание                              |
|--------------------------------|---------------------------------------|
| `/db/create/user`              | Создание юзера                        |
| `db/user_info?user_id={id}`    | Получение неполной информации о юзере |
| `db/user_info_all?user_id{id}` | Получение полной информации о юзере   |

## API Details

### 1. Создание юзера
**URL**: `db/create_user`
**Method**: `POST`

**Request Body**:
```json
{
  "login": "string",
  "hashed_password": "string",
  "email": "string"
}
```

**Responce**:
```json
{
  "status": "success"
}
```

**Responce(если юзер не найден)**:
```json
{
  "error": "not found"
}
```

### 2. Получение неполной информации о юзере
**URL**: `/db/user_info?user_id={id}`
**Method**: `GET`

**Responce**:
```json
{
  "login": "string",
  "hashed_password": "string",
  "email": "string",
  "is_active": true
}
```

### 3. Получение полной информации о юзере
**URL**: `/user_info_all?user_id={id}`
**Method**: `GET`

**Responce**:
```json
{
  "email": "string",
  "login": "string",
  "hashed_password": "string",
  "registered_at": "datetime",
  "date_knockout": "datetime",
  "profile_img": "string",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

**Responce(если юзер не найден)**:
```json
{
  "error": "not found"
}
```