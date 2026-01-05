import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("service.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://faceattendancerealtime-3c8bc-default-rtdb.firebaseio.com/'
})

ref = db.reference('Students')

#data add#
data = {
    "1":
        {
            "name": "Sagar Panwar",
            "major": "AIML",
            "starting_year": 2022,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2025-12-11 00:54:34"
        },
    "2":
        {
            "name": "Anuj Sharma",
            "major": "AIML",
            "starting_year": 2022,
            "total_attendance": 0,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2025-12-11 00:54:34"
        },
    "3":
        {
            "name": "Prashant Purohit",
            "major": "Economics",
            "starting_year": 2023,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2025-12-11 00:54:34"
        },
    "4":
        {
            "name": "Elon Musk",
            "major": "Economics",
            "starting_year": 2022,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2025-12-11 00:54:34"
        },
    "5":
        {
            "name": "Ayush Rawat",
            "major": "Physics",
            "starting_year": 2023,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2025-12-11 00:54:34"
        },
    "6":
        {
            "name": "Tiwari ji",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2025-12-11 00:54:34"
        },
    "7":
        {
            "name": "Utkarsh Ram",
            "major": "Physics",
            "starting_year": 2018,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2025-12-11 00:54:34"
        },
    "9":
        {
            "name": "Sarthak Bisht",
            "major": "Physics",
            "starting_year": 2019,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2025-12-11 00:54:34"
        },
    "10":
        {
            "name": "Ankur Chauhan",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2025-12-11 00:54:34"
        },
    "11":
        {
            "name": "Lakshay Dimri",
            "major": "Physics",
            "starting_year": 2022,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2025-12-11 00:54:34"
        },
    "12":
        {
            "name": "Vikas Negi",
            "major": "Physics",
            "starting_year": 2024,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2025-12-11 00:54:34"
        },
    "13":
        {
            "name": "Sakshi Goyal",
            "major": "Physics",
            "starting_year": 2022,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2025-12-11 00:54:34"
        },
    "14":
        {
            "name": "Dev Sharma",
            "major": "Physics",
            "starting_year": 2022,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2025-12-11 00:54:34"
        },
    "15":
        {
            "name": "Bhoomika Rawat",
            "major": "Physics",
            "starting_year": 2025,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2025-12-11 00:54:34"
        }
}
for key,value in data.items():
    ref.child(key).set(value)