MINIO_PUBLIC_BASE_URL = "http://localhost:9000/beam-images/"

CONCRETE_GRADES = [
    {
        "id": 1,
        "grade_code": "M100",
        "name": "М100",
    "base_description": "Дешевый и хрупкий",
        "compressive_strength_mpa": 0.50,
        "image_key": "m100.jpg",
        "image_url": f"{MINIO_PUBLIC_BASE_URL}m100.jpg",
    },
    {
        "id": 2,
        "grade_code": "M150",
        "name": "М150",
    "base_description": "Недорогой и практичный",
        "compressive_strength_mpa": 0.83,
        "image_key": "m150.jpg",
        "image_url": f"{MINIO_PUBLIC_BASE_URL}m150.jpg",
    },
    {
        "id": 3,
        "grade_code": "M200",
        "name": "М200",
    "base_description": "Надежный и популярный",
        "compressive_strength_mpa": 1.00,
        "image_key": "m200.jpg",
        "image_url": f"{MINIO_PUBLIC_BASE_URL}m200.jpg",
    },
    {
        "id": 4,
        "grade_code": "M250",
        "name": "М250",
    "base_description": "Универсальный и крепкий",
        "compressive_strength_mpa": 1.33,
        "image_key": "m250.jpg",
        "image_url": f"{MINIO_PUBLIC_BASE_URL}m250.jpg",
    },
    {
        "id": 5,
        "grade_code": "M300",
        "name": "М300",
    "base_description": "Прочный и долговечный",
        "compressive_strength_mpa": 1.50,
        "image_key": "m300.jpg",
        "image_url": f"{MINIO_PUBLIC_BASE_URL}m300.jpg",
    },
]

CALCULATIONS = {
    1: {
        "id": 1,
        "beam_length_m": 6.0,
        "beam_width_mm": 200,
        "beam_height_mm": 300,
        "result_max_load_kN": 125.0,
        "selected_grades": [
            {"grade_id": 2, "quantity": 1, "order_index": 1, "is_primary": True, "comment": "Основная марка"},
            {"grade_id": 4, "quantity": 2, "order_index": 2, "is_primary": False, "comment": "Альтернативный вариант"},
        ],
    }
}
