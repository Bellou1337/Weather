# FastAPI Database API

## API Endpoints

| Метод                                                                             | Описание
|-----------------------------------------------------------------------------------|----------------------------------------------|
| [`/db/user_info?user_id={id}`](#1-получение-неполной-информации-о-пользователе)   | Получение неполной информации о пользователе |
| [`/db/user_info_all?user_id={id}`](#2-получение-полной-информации-о-пользователе) | Получение полной информации о пользователе   |
| [`/db/user_img?user_id={id}`](#3-получение-пути-фотографии-пользователя)          | Получение пути фотографии пользователя       |
| [`/db/user_request?user_id={id}`](#4-получение-реквестов-по-id)                   | Получение пути фотографии пользователя       |
| [`/db/change_password`](#5-изменение-пароля)                                      | Изменение пароля                             |
| [`/db/change_img`](#6-изменение-фотографии)                                       | Изменение фотографии                         |
| [`/db/change_email`](#7-изменение-почты)                                          | Изменение почты                              |

## API Details

### 1. Получение неполной информации о пользователe
**URL**: `/db/user_info?user_id={id}`
**Method**: `GET`

**Response**:
```json
{
  "login": "string",
  "hashed_password": "string",
  "email": "string",
  "is_active": "boolean"
}
```

**Response (если пользователь не найден)**:
```json
{
  "error": "user not found"
}
```

### 2. Получение полной информации о пользователe
**URL**: `/user_info_all?user_id={id}`
**Method**: `GET`

**Response**:
```json
{
  "email": "string",
  "login": "string",
  "hashed_password": "string",
  "registered_at": "datetime",
  "date_knockout": "datetime",
  "profile_img": "string",
  "is_active": "boolean",
  "is_superuser": "boolean",
  "is_verified": "boolean"
}
```

**Response (если пользователь не найден)**:
```json
{
  "error": "user not found"
}
```

### 3. Получение пути фотографии пользователя
**URL**: `/db/user_img?user_id{id}`
**Method**: `GET`

**Response**:
```json
{
  "profile_img": "string",
  "login": "string"
}
```

**Response (если пользователь не найден)**:
```json
{
  "error": "user not found"
}
```

### 4. Получение реквестов по id
**URL**: `/db/user_request?user_id{id}`
**Method**: `GET`

**Response**:
```json
{
  [
    {
      "city_name": "string",
      "date_request": "datetime",
      "Response": "JSON"
    }
  ]
}
```

**Response (если пользователь не найден)**:
```json
{
  "error": "user not found"
}
```

### 5. Изменение пароля
**URL**: `/db/change_password`
**Method**: `POST`


**Request Body**:
```json
{
  "user_id": "int",
  "new_password": "string"
}
```

**Response**:
```json
{
  "status": "password update"
}
```

**Response (если пользователь не найден)**:
```json
{
  "detail": "user not found"
}
```

### 6. Изменение фотографии
**URL**: `/db/change_img`
**Method**: `POST`


**Request Body**:
```json
{
  "user_id": "int",
  "new_img_path": "string"
}
```

**Response**:
```json
{
  "status": "image update"
}
```

**Response (если пользователь не найден)**:
```json
{
  "detail": "user not found"
}
```

### 7. Изменение почты
**URL**: `/db/change_email`
**Method**: `POST`


**Request Body**:
```json
{
  "user_id": "int",
  "new_email": "string"
}
```

**Response**:
```json
{
  "status": "email update"
}
```

**Response (если пользователь не найден)**:
```json
{
  "detail": "user not found"
}
```