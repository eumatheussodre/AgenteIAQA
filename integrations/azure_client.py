from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

class AzureDevOpsClient:
    def __init__(self, organization_url, personal_access_token, project):
        credentials = BasicAuthentication('', personal_access_token)
        self.connection = Connection(base_url=organization_url, creds=credentials)
        self.project = project
        self.wit_client = self.connection.clients.get_work_item_tracking_client()

    def criar_test_case(self, titulo, passos):
        print("Criando Test Case no Azure DevOps...")
        try:
            document = [
                {"op": "add", "path": "/fields/System.Title", "value": titulo},
                {"op": "add", "path": "/fields/Microsoft.VSTS.TCM.Steps", "value": passos}
            ]
            result = self.wit_client.create_work_item(
                document=document,
                project=self.project,
                type="Test Case"
            )
            print(f"✅ Test Case criado: {result.id}")
            return result.id
        except Exception as e:
            print(f"❌ Erro ao criar Test Case: {e}")
            return None
