def test_get_assignments_student_1(client, h_student_1):
    """ Test to get the list of assignments for student 1 """
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    """ Test to get list of assignments for Student 2 """
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2

def test_post_assignment_student_1(client, h_student_1):
    """ Test to update the assignment"""
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1):
    """ Test to submit the assignment for correct student under Teacher ID 2 """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2

# def test_submit_assignment_student_1(client, h_student_1):
    """ Test to submit the assignment for wrong assignment ID """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 20,
            'teacher_id': 2
        })

    error_response = response.json
    assert response.status_code == 404
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'No assignment with this id was found'

def test_assingment_resubmitt_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'

def test_assingment_resubmitt_error(client, h_student_1):
    ''' Failure Test Case - Bad Request '''
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacherID': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'ValidationError'
    assert error_response["message"]["teacher_id"] == [
            "Missing data for required field."
        ]

def test_assingment_upsert_failure(client, h_student_1):
    ''' Failure Test Case for updating an assignment that doesn't exist - Bad Request '''
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            "id":10,
            "content": "some text"
        })
    error_response = response.json
    assert response.status_code == 404
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == "No assignment with this id was found"

def test_assingment_edit_failure(client, h_student_1):
    ''' Failure Test Case for updating an assignment in Submitted state - Bad Request '''
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            "id":1,
            "content": "some text"
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == "only assignment in draft state can be edited"