import requests # to call the endpoint from the Python, WE need requests.interact with HTTP direct from python
import uuid # to generate random numstring
ENDPOINT = "https://todo.pixegami.io"

# response = requests.get(ENDPOINT) # we call this and it wil return the response object

# # print the response object
# print("Response: ", response)

# # to print out the data inside the response object
# data = response.json()
# print(data)

# # print the status code of the response object
# status_code = response.status_code
# print(status_code)

# testing the endpoint if its working and it we can call it.
def test_can_call_endpoint():
    """
    to test if we can reach the endpoint.
    used assert to see if the response its green light
    if the endpoint its working, the response status code will give response of 200
    if the assert failed, it will throw an exception
    the test will pass if the response code equal to 200.
    """
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_create_task():
    """
    to test if we can create a task using the create_task endpoint
    if the endpoint its working, the response status code will give response of 200
    we will send the request body to the endpoint
    and see if we can get the response out of it.
    """
    # payload = {
    #     "content": "my test content",
    #     "user_id": "test_user",
    #     "task_id": "test_tast_id",
    #     "is_done":  False
    # }

    # we can also refractor this payload and become helper function
    payload = new_task_payload()

    # create_task_response = requests.put(ENDPOINT+"/create-task",json=payload)
    # we can refractor the code above here by calling the create_task() function
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200

    data = create_task_response.json()
    # print(data)

    # how do we ensure the task we created is exist?
    # next, we can check the task that create by get the task_id
    task_id = data["task"]["task_id"]
    #get_task_response = requests.get(ENDPOINT + f"/get-task/{task_id}") # same goes here. we can refractor the code by calling get_task() function
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200

    get_task_data = get_task_response.json()
    # print(get_task_data) # if not sure, print it and check it out.
    """
    output from get_task_response
    {'is_done': False, 'content': 'my test content', 'user_id': 'test_user', 
    'task_id': 'task_03cfb49190ed4922b67ad7c20e4b9c82', 'ttl': 1703298475, 'created_time': 1703212075}

    since we can access the task_id from the create_task_response object,
    we can access all the 'content', 'user_id' and 'is_done' key fields.
    """
    # we can check if the response the we get from the endpoint
    # is similar to what we had pass.
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]

    # we can also assert to something not from the real value for sanity check
    # we can assert to fail the test.

    # assert get_task_data["content"] != "some other content"

def test_can_update_task():
    # create a task # notice some of the function code might get reused here
    payload = new_task_payload()
    create_task_response = create_task(payload)
    task_id = create_task_response.json()["task"]["task_id"]

    # update the task
    new_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "my updated content",
        "is_done": True
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200 # check if the response works

    # get and validate the changes
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data ["is_done"] == new_payload["is_done"]

def test_can_list_tasks():
    """
    to test if the response can list all the tasks that we 
    had created earlier. here we can check the number of tasks we had created
    is similar from the response object
    """
    payload = new_task_payload()

    # create N tasks
    n = 3
    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    # list tasks, and check that there N items
    user_id = payload["user_id"]
    list_tasks_response = list_tasks(user_id)
    assert list_tasks_response.status_code == 200
    data = list_tasks_response.json()
    assert len(data["tasks"]) == n
    # print(data)

def test_can_delete_task():
    """
    to test if the response can delete task that 
    had created earlier. here we can check the status code on the 
    deleted task. it should return 404 status code meaning task not found.
    """
    # create the task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]
    # delete the task
    del_response = delete_task(task_id)
    assert del_response.status_code == 200
    # check the deleted task
    check_del_response = get_task(task_id)
    assert check_del_response.status_code == 404

def create_task(payload):
    return requests.put(ENDPOINT + "/create-task",json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def list_tasks(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")

def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}" # pick random uuid. its an object. use hex to return as string
    content = f"test_content_{uuid.uuid4().hex}"
    
    # print(f"Creating task for user {user_id} with content {content}")
    return {
        "content": content,
        "user_id": user_id,
        "is_done":  False
    }
def update_task(payload):
    return requests.put(ENDPOINT + "/update-task",json=payload)

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")


