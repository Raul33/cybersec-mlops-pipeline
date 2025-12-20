from prefect import flow, task

@task
def hello_task():
    return "Prefect está funcionando correctamente 🚀"

@flow(name="data_ingestion_flow")
def data_ingestion_flow():
    result = hello_task()
    print(result)

if __name__ == "__main__":
    data_ingestion_flow()
