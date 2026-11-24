# Lista de Tarefas — Flask + Docker + Render

CRUD simples de tarefas com Flask, PostgreSQL e Docker, publicado no Render.

## Estrutura
```
lista-tarefas/
├── app.py
├── templates/        (index.html, editar.html)
├── static/           (style.css)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── render.yaml
└── README.md
```

## Rodar localmente (Docker Compose)
```bash
docker compose up --build
```
Acesse http://localhost:8000

Parar: `docker compose down` (use `-v` para apagar o banco).

## Endpoints
| Rota | Descrição |
|------|-----------|
| `/` | Interface web (CRUD) |
| `/api/tarefas` | Lista as tarefas em JSON |
| `/health` | Health check usado pelo Render |

## Deploy no Render
1. Crie um repositório no GitHub e envie o projeto:
   ```bash
   git init && git add . && git commit -m "Primeiro commit"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/lista-tarefas.git
   git push -u origin main
   ```
2. Em https://render.com, crie uma conta e conecte o GitHub.
3. Clique em **New → Blueprint**, escolha o repositório e confirme.
   O Render lê o `render.yaml`, constrói o Dockerfile e cria o PostgreSQL.
4. Quando o status ficar **Live**, abra a URL `https://lista-tarefas-xxxx.onrender.com`.

### Deploy manual (sem Blueprint)
1. **New → PostgreSQL** (plano Free) e copie a *Internal Database URL*.
2. **New → Web Service** → repositório → Runtime **Docker** → plano Free.
3. Em *Environment*, crie `DATABASE_URL` com a URL copiada.
4. Em *Advanced*, defina o Health Check Path como `/health`.

## Observações do Free Tier
- O serviço web gratuito "dorme" após ~15 min sem acessos; o primeiro acesso depois disso demora ~1 min. **Abra a URL antes de apresentar.**
- O PostgreSQL gratuito tem prazo de validade; confira as regras atuais em render.com/pricing.
