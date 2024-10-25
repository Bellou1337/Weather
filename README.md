# FastAPI Database API

## API Endpoints

| Метод                           | Описание                              |
|---------------------------------|---------------------------------------|
| `/db/create/user`               | Создание юзера                        |
| `/db/user_info?user_id={id}`    | Получение неполной информации о юзере |
| `/db/user_info_all?user_id{id}` | Получение полной информации о юзере   |
| `/db/user_img?user_id{id}`      | Получение пути фотографии юзера       |
| `/db/user_request?user_id{id}`  | Получение реквестов по id             |
| `/db/change_password`           | Изменение пароля                      |
| `/db/change_img`                | Изменение фотографии                  |
| `/db/change_email`              | Изменение почты                       |

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

### 4. Получение пути фотографии юзера
**URL**: `/db/user_img?user_id{id}`
**Method**: `GET`

**Responce**:
```json
{
  "profile_img": "string",
  "login": "string"
}
```

**Responce(если юзер не найден)**:
```json
{
  "error": "not found"
}
```

### 5. Получение реквестов по id
**URL**: `/db/user_request?user_id{id}`
**Method**: `GET`

**Responce**:
```json
{
  [
    {
      "city_name": "string",
      "date_request": "datetime",
      "responce": "JSON"
    }
  ]
}
```

**Responce(если юзер не найден)**:
```json
{
  "error": "not found"
}
```

### 6. Изменение пароля
**URL**: `/db/change_password`
**Method**: `POST`


**Request Body**:
```json
{
  "user_id": "int",
  "new_password": "string"
}
```

**Responce**:
```json
{
  "status": "password update"
}
```

**Responce(если юзер не найден)**:
```json
{
  "detail": "User not found"
}
```

### 7. Изменение фотографии
**URL**: `/db/change_img`
**Method**: `POST`


**Request Body**:
```json
{
  "user_id": "int",
  "new_img_path": "string"
}
```

**Responce**:
```json
{
  "status": "image update"
}
```

**Responce(если юзер не найден)**:
```json
{
  "detail": "User not found"
}
```

### 8. Изменение почты
**URL**: `/db/change_email`
**Method**: `POST`


**Request Body**:
```json
{
  "user_id": "int",
  "new_email": "string"
}
```

**Responce**:
```json
{
  "status": "email update"
}
```

**Responce(если юзер не найден)**:
```json
{
  "detail": "User not found"
}
```