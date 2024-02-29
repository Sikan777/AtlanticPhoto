# AtlanticPhoto

<p align="center">
  <img src="https://res.cloudinary.com/dclbglorh/image/upload/v1709217303/atlantic_imlcz2.png"
  alt="AtlanticPhoto" width="256" height="256">
</p>

---

AtlanticPhoto is an app that allows you to share and see others activities without any cheat all over the world.
It's so pure and transparent as if you were in an ocean, so enjoy it :)

---

[![Documentation Status](https://readthedocs.org/projects/atlanticphoto/badge/?version=latest)](https://atlanticphoto.readthedocs.io/en/latest/?badge=latest)

## Table of Contents

- [Technologies](#technologies)
- [Basic functionality](#basic-functionality)
  - [Authentication](#authentication)
  - [Working with photos](#working-with-photos)
  - [Comments](#comments)
- [Usage](#usage)
  - [Installation](#installation)
  - [Additional information](#additional-information)
- [License](#license)
- [Authors](#authors)

## Technologies

| **Module**                                                     | **Description**    |
| -------------------------------------------------------------- | ------------------ |
| [FastAPI](https://fastapi.tiangolo.com/)                       | Framework          |
| [Pydantic](https://pydantic-docs.helpmanual.io/)               | Validation library |
| [SQLAlchemy](https://docs.sqlalchemy.org/)                     | ORM                |
| [Alembic](https://alembic.sqlalchemy.org/en/latest/)           | Migration tool     |
| [PostgreSQL](https://www.postgresql.org/)                      | Database           |
| [Cloudinary](https://cloudinary.com/)                          | Image hosting      |
| [FastAPI-limiter](https://github.com/long2ice/fastapi-limiter) | Rate limiting      |
| [Passlib](https://passlib.readthedocs.io/en/stable/)           | Password hashing   |
| [Qrcode](https://pypi.org/project/qrcode/)                     | QR code generator  |
| [Pillow](https://pypi.org/project/Pillow/)                     | Image processing   |

## Basic functionality

### Authentication

**Endpoints:**

```
POST /api/auth/signup
```

```
POST /api/auth/login
```

```
POST /api/auth/logout
```

```
POST /api/auth/refresh_token
```

_The names speak for themselves_

The application uses JWT tokens for authentication. Users have three roles: regular user, moderator, and administrator.
The first user is an administrator.

To implement different access levels (regular user, moderator, and administrator),
FastAPI decorators are used to check the token and user role.

### Working with photos

**Users can perform various operations related to photos:**

- Upload photos with descriptions.
  ```
  POST /api/images/
  ```
- Delete photos.
  ```
  DELETE /api/images/{image_id}
  ```
- Edit photo descriptions.
  ```
  PATCH /api/images/{image_id}
  ```
- Retrieve a photo by a unique id.
  ```
  GET /api/images/{image_id}
  ```
- Add up to 5 tags per photo.

- Retrieve all your photos.

  ```
  GET /api/images/
  ```

- Apply basic photo transformations using
  [Cloudinary services](https://cloudinary.com/documentation/image_transformations).
  ```
  POST /api/transform/create_transformed/{original_image_id}
  ```
- Generate links to transformed images for viewing as URL and QR-code. Links are stored on the server.

  ```
  POST /api/transform/{transformed_pic_id}/qr
  ```

- Retrieve a transformed photo by a unique id.

  ```
  GET /api/transform/{transformed_pic_id}
  ```

- Retrieve all your transformed photos.

  ```
  GET /api/transform/{user_id}/transformed
  ```

- Update parameters of an existed transformed picture.

  ```
  PATCH /api/transform/{transformed_pic_id}/
  ```

- Delete an existed transformed picture.
  ```
  DELETE /api/transform/{transformed_pic_id}/
  ```
  Administrators can perform all CRUD operations with user photos.

### Comments

**Under each photo, there is a comment section. Users can:**

- Add and read comments to each other's photos.

  ```
  POST /api/comments/
  ```

- Edit comment.
  ```
  PATCH /api/comments/{comment_id}
  ```
- Administrators and moderators [if you have the role](#authentication) can delete comments.
  ```
  DELETE /api/comments/{comment_id}
  ```

### Profile

**Endpoints for user profile:**

- See users profiles.
  ```
  GET /api/users/{username}
  ```

## Usage

### Installation

- Clone the repository.

```Shell
  git clone https://github.com/Sikan777/AtlanticPhoto
```

- Install dependencies.

```Shell
  pip install -r requirements.txt
```

_or with poetry_

```Shell
  poetry install
```

- Setup the ".env" file.

```Shell
  cp .env.example .env
```

_and fill in the information you need_

- Run the application.

```Shell
  uvicorn main:app --reload
```

- Enjoy!

### Additional information

- [Documentation](https://pythongram.readthedocs.io/en/latest/)
- [Swagger documentation(soon)](https://python-gram-secure-organization.koyeb.app/docs)
- [GitHub](https://github.com/Sikan777/AtlanticPhoto)

## License

This project is licensed under the [MIT License](https://github.com/Sikan777/AtlanticPhoto/blob/main/LICENSE).

## Authors

- [Sikan777](https://github.com/Sikan777)
- [Sapientus](https://github.com/Sapientus)
- [OlgaTsuban](https://github.com/OlgaTsuban)
- [hedgyv](https://github.com/hedgyv)
- [Artem650](https://github.com/Artem650)

Feel free to provide feedback, report issues, or contribute to the project!
