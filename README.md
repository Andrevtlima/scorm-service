# SCORM Service

Este repositório contém um micro-serviço para hospedar e executar cursos SCORM 2004. O serviço é baseado em [FastAPI](https://fastapi.tiangolo.com/) e usa PostgreSQL para persistência e um bucket GCS (via MinIO) para armazenar o conteúdo dos cursos.

## Funcionalidades
- Upload de pacotes SCORM (`imsmanifest.xml`) com injeção automática do script `scorm-hook.js`.
- Versionamento e exclusão lógica de cursos.
- Criação de registros de execução (registrations) por aluno e curso.
- Geração de URLs de lançamento assinadas por HMAC.
- Player que valida a assinatura e atualiza o status da execução.
- Estrutura básica para webhooks e painel admin.

## Requisitos
- Python 3.11
- PostgreSQL
- MinIO configurado como Gateway para GCS (ou outro bucket compatível).

## Execução rápida
A forma mais simples de subir o ambiente é usando `docker-compose`:

```bash
docker-compose up --build
```

O script `scripts/init_db.py` cria as tabelas e um API Key de demonstração (`x-api-key-123`).

## Variáveis de Ambiente
- `DATABASE_URL`: URL de conexão do PostgreSQL.
- `MINIO_ENDPOINT`: endpoint do MinIO.
- `MINIO_BUCKET`: nome do bucket onde os cursos são armazenados.
- `MINIO_ACCESS_KEY` / `MINIO_SECRET_KEY`: credenciais do bucket.
- `MINIO_MODE`: valor "gcs" para usar gateway GCS.
- `API_KEY_SECRET`: segredo utilizado na geração da assinatura do Launch URL.

## Endpoints Principais
- `POST /courses/upload` - Faz o upload de um pacote zipado para um `course_id`.
- `GET /courses` - Lista os cursos ativos.
- `DELETE /courses/{course_id}` - Marca o curso como removido (soft delete).
- `POST /registrations` - Cria ou obtém uma inscrição para `learner_id` e `course_id`.
- `GET /launch-url` - Retorna uma URL de lançamento assinada para o player.
- `GET /player` - Endpoint que valida a assinatura e redireciona para o `index.html` do curso.

Todos os endpoints requerem o cabeçalho `x-api-key` com uma chave válida.

## Desenvolvimento
1. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
2. Exporte as variáveis de ambiente conforme `.env.example` (crie esse arquivo se necessário).
3. Inicialize o banco de dados:
    ```bash
    python scripts/init_db.py
    ```
4. Inicie a aplicação:
    ```bash
    uvicorn app.api.main:app --reload
    ```

## Licença
Distribuído sob a licença MIT.

