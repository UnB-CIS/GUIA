# Roadmap de Desenvolvimento

## Backlog de Issues

### Infraestrutura & DevOps (guia-infra)

-   `[Infra] 1:` Configurar ambiente de desenvolvimento local com Docker Compose.
-   `[Infra] 2:` Estruturar pipeline de CI base com GitHub Actions.
-   `[Infra] 3:` Escrever Dockerfile e pipeline de CI para `guia-backend`.
-   `[Infra] 4:` Escrever Dockerfile e pipeline de CI para `guia-report-processing`.
-   `[Infra] 5:` Escrever Dockerfile e pipeline de CI para `guia-routing-engine`.
-   `[Infra] 6:` Provisionar cluster Kubernetes (K8s) e configurar acesso `kubectl`. **CURVA DE APRENDIZAGEM**
-   `[Infra] 7:` Criar manifestos K8s (Deployment, Service, ConfigMap) para `guia-backend`. **CURVA DE APRENDIZAGEM**
-   `[Infra] 8:` Criar manifestos K8s para `guia-report-processing`.  **CURVA DE APRENDIZAGEM**
-   `[Infra] 9:` Criar manifestos K8s para `guia-routing-engine` (com PersistentVolumeClaim). **CURVA DE APRENDIZAGEM**
-   `[Infra] 10:` Configurar NGINX Ingress Controller para roteamento de APIs.
-   `[Infra] 11:` Configurar segredos (secrets) no K8s para credenciais. **CURVA DE APRENDIZAGEM**
-   `[Infra] 12:` Implementar deploy de Prometheus e Grafana para monitoramento **OPICIONAL**

### Banco de Dados (guia-db)

-   `[Dados] 1:` Modelagem do Banco de dados com `schemas` e `configs` do PostGIS.
-   `[Dados] 2:` Finalizar e commitar schema do PostGIS (tabelas: `users`, `reports`, `h3_risk_index`).
-   `[Dados] 3:` Implementar pipeline de migração de schema (ex: com Alembic).
-   `[Dados] 4:` Desenvolver script para popular a tabela `h3_risk_index` com a geometria da grade H3.

### Backend (guia-backend)

-   `[Backend] 1:` Implementar endpoints de autenticação JWT (`/auth/register`, `/auth/login`).
-   `[Backend] 2:` Proteger endpoints da aplicação com middleware de autenticação JWT.
-   `[Backend] 3:` Implementar endpoint `POST /api/reports` para receber metadados de ocorrências.
-   `[Backend] 4:` Implementar endpoint para gerar URL de upload pré-assinada para o Object Storage.
-   `[Backend] 5:` Implementar a publicação de mensagem na fila (RabbitMQ) após confirmação do upload. **CURVA DE APRENDIZAGEM**
-   `[Backend] 6:` Implementar endpoint `GET /api/heatmap` para servir dados da tabela `h3_risk_index`.

### Processamento de Reports com IA (guia-report-processing)

-   `[IA] 1:` Construir o consumidor da fila para escutar novas tarefas de processamento.
-   `[IA] 2:` Implementar a integração com o modelo Image-to-Text.
-   `[IA] 3:` Implementar a integração com o modelo de Extração de Informação.
-   `[IA] 4:` Implementar o algoritmo para cálculo do `risk_score`.
-   `[IA] 5:` Implementar a lógica para salvar/atualizar o `risk_score` na tabela `h3_risk_index`.

### Motor de Roteamento (guia-routing-engine)

-   `[Rota] 1:` Fazer um fork do repositório oficial do Valhalla.
-   `[Rota] 2:` Realizar profiling de performance para identificar gargalos no código C++.
-   `[Rota] 3:` Refatorar o código para remover perfis de custo não utilizados (ex: bicicleta, pedestre).
-   `[Rota] 4:` Pesquisar a viabilidade de modificar o `GraphBuilder` em C++ para consultar o PostGIS diretamente.
-   `[Rota] 5:` Definir o contrato da API (`/route`) com OpenAPI/Swagger.
-   `[Rota] 6:` Estruturar o serviço de API.
-   `[Rota] 7:` Implementar a validação de entrada da requisição.
-   `[Rota] 8:` Implementar a lógica de proxy para o processo Valhalla.
-   `[Rota] 9:` Implementar tratamento de erros e timeouts do Valhalla.
-   `[Rota] 10:` Implementar endpoint de health check (`/healthz`). **CURVA DE APRENDIZAGEM**
-   `[Rota] 11:` Instrumentar o serviço com métricas Prometheus. **OPICIONAL**
-   `[Rota] 12:` Escrever suíte de testes de integração para o fluxo da API.

### Map Builder (Job Assíncrono - map-builder)

-   `[Builder] 1:` Criar script `enrich_osm_with_risk.py`.
-   `[Builder] 2:` Criar script `valhalla_build_tiles.sh`.
-   `[Builder] 3:` Criar o workflow de GitHub Actions agendado (Cron). **CURVA DE APRENDIZAGEM**
-   `[Builder] 4:` Adicionar passo ao workflow para upload do `valhalla_tiles.tar` para Object Storage.
-   `[Builder] 5:` Adicionar passo ao workflow para disparar o Rolling Update via `kubectl apply`.

### Aplicativo Mobile (guia-mobile)

-   `[Mobile] 1:` Implementar telas e fluxo de autenticação.
-   `[Mobile] 2:` Implementar fluxo de submissão de reports.
-   `[Mobile] 3:` Implementar a interface do mapa (com H3 Uber, utilizar exemplo da 99).
-   `[Mobile] 4:` Implementar a UI para solicitar uma rota.
-   `[Mobile] 5:` Implementar a chamada ao `GET /api/route` e desenhar a polilinha no mapa.

### Dashboard Web (guia-web)

-   `[Web] 1:` Estruturar o projeto base do dashboard (ex: com React, ou HTML puro).
-   `[Web] 2:` Implementar a interface do H3.
-   `[Web] 3:` Implementar a lógica para consumir o endpoint `GET /api/H3`.

### Qualidade, Segurança & Documentação **CURVA DE APRENDIZAGEM**

-   `[QA] 1:` Definir e documentar a estratégia de testes (Unit, Integration, E2E).
-   `[QA] 2:` Implementar suíte de testes E2E que simula o fluxo completo.
-   `[SEC] 1:` Configurar políticas de segurança no Ingress (ex: Rate Limiting).
-   `[SEC] 2:` Implementar Network Policies no K8s para restringir a comunicação entre serviços.
-   `[DOC] 1:` Gerar e publicar a documentação da API (via OpenAPI/Swagger).

## Plano de Sprints (2 semanas por Sprint)

### Sprint 1: Fundação
- `[Infra] 1:` Configurar ambiente de desenvolvimento local.
- `[Dados] 1:` Modelagem do Banco de dados.

### Sprint 2: Schema e Migração
- `[Dados] 2:` Finalizar e commitar schema do PostGIS.
- `[Dados] 3:` Implementar pipeline de migração de schema.

### Sprint 3: CI e Autenticação
- `[Infra] 2:` Estruturar pipeline de CI base.
- `[Backend] 1:` Implementar endpoints de autenticação JWT.

### Sprint 4: Dockerização do Backend
- `[Infra] 3:` Escrever Dockerfile e pipeline de CI para `guia-backend`.
- `[Backend] 2:` Proteger endpoints com middleware JWT.

### Sprint 5: Início da Ingestão de Reports
- `[Backend] 3:` Implementar endpoint `POST /api/reports`.
- `[Backend] 4:` Implementar endpoint para gerar URL de upload pré-assinada.

### Sprint 6: Fila de Processamento
- `[Backend] 5:` Implementar a publicação de mensagem na fila (RabbitMQ).
- `[IA] 1:` Construir o consumidor da fila.

### Sprint 7: Dockerização da IA
- `[Infra] 4:` Escrever Dockerfile e pipeline de CI para `guia-report-processing`.
- `[IA] 5:` Implementar a lógica para salvar/atualizar `risk_score` (mockado).

### Sprint 8: Autenticação Mobile
- `[Mobile] 1:` Implementar telas e fluxo de autenticação.
- `[DOC] 1:` Gerar e publicar a documentação da API.

### Sprint 9: Submissão de Reports Mobile
- `[Mobile] 2:` Implementar fluxo de submissão de reports.
- `[IA] 2:` Implementar a integração com o modelo Image-to-Text.

### Sprint 10: IA - Extração de Info
- `[IA] 3:` Implementar a integração com o modelo de Extração de Informação.
- `[IA] 4:` Implementar o algoritmo para cálculo do `risk_score`.

### Sprint 11: Fundação de Roteamento
- `[Infra] 5:` Escrever Dockerfile e pipeline de CI para `guia-routing-engine`.
- `[Rota] 5:` Definir o contrato da API (`/route`).

### Sprint 12: Estrutura da API de Rota
- `[Rota] 6:` Estruturar o serviço de API.
- `[Rota] 8:` Implementar a lógica de proxy para o processo Valhalla.

### Sprint 13: Validação e Erros de Rota
- `[Rota] 7:` Implementar a validação de entrada da requisição.
- `[Rota] 9:` Implementar tratamento de erros e timeouts do Valhalla.

### Sprint 14: População de Dados e Mapa Mobile
- `[Dados] 4:` Desenvolver script para popular a tabela `h3_risk_index`.
- `[Mobile] 3:` Implementar a interface do mapa.

### Sprint 15: Início do Map Builder
- `[Builder] 1:` Criar script `enrich_osm_with_risk.py`.
- `[Builder] 2:` Criar script `valhalla_build_tiles.sh`.

### Sprint 16: Automação do Build
- `[Builder] 3:` Criar o workflow de GitHub Actions agendado.
- `[Builder] 4:` Adicionar passo para upload do artefato.

### Sprint 17: UI de Rota e Deploy do Builder
- `[Builder] 5:` Adicionar passo para disparar o Rolling Update.
- `[Mobile] 4:` Implementar a UI para solicitar uma rota.

### Sprint 18: Conexão Final (MVP)
- `[Mobile] 5:` Implementar a chamada ao `GET /api/route` e desenhar a polilinha.
- `[QA] 1:` Definir e documentar a estratégia de testes.

### Sprint 19: Fundação K8s
- `[Infra] 6:` Provisionar cluster Kubernetes (K8s).
- `[Infra] 11:` Configurar segredos (secrets) no K8s.

### Sprint 20: Deploy no K8s (Backend & IA)
- `[Infra] 7:` Criar manifestos K8s para `guia-backend`.
- `[Infra] 8:` Criar manifestos K8s para `guia-report-processing`.

### Sprint 21: Deploy no K8s (Rota & Ingress)
- `[Infra] 9:` Criar manifestos K8s para `guia-routing-engine`.
- `[Infra] 10:` Configurar NGINX Ingress Controller.

### Sprint 22: Testes e Saúde do Sistema
- `[Rota] 10:` Implementar endpoint de health check.
- `[Rota] 12:` Escrever suíte de testes de integração.

### Sprint 23: Segurança e Testes E2E
- `[QA] 2:` Implementar suíte de testes E2E.
- `[SEC] 1:` Configurar políticas de segurança no Ingress.

### Sprint 24: Segurança de Rede
- `[SEC] 2:` Implementar Network Policies no K8s.
- `[Web] 1:` Estruturar o projeto base do dashboard.

### Sprint 25: Dashboard Web
- `[Web] 2:` Implementar a interface do H3.
- `[Backend] 6:` Implementar endpoint `GET /api/heatmap`.

### Sprint 26: Finalização do Dashboard
- `[Web] 3:` Implementar a lógica para consumir o endpoint `GET /api/H3`.
- `[Infra] 12:` Implementar deploy de Prometheus e Grafana.

### Sprint 27: Métricas e Fork Valhalla (Pós-MVP)
- `[Rota] 11:` Instrumentar o serviço com métricas Prometheus.
- `[Rota] 1:` Fazer um fork do repositório oficial do Valhalla.

### Sprint 28: Análise Valhalla (Pós-MVP)
- `[Rota] 2:` Realizar profiling de performance.
- `[Rota] 3:` Refatorar para remover perfis de custo não utilizados.

### Sprint 29: P&D Valhalla (Pós-MVP)
- `[Rota] 4:` Pesquisar viabilidade de modificar o `GraphBuilder`.

---

**Duração Total Estimada:** 29 Sprints de 2 semanas = **58 semanas** ~= **15 meses**.