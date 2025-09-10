# Roadmap de Desenvolvimento

O projeto é gerenciado em Sprints de 2 semanas. A tabela abaixo resume as metas e os entregáveis chave para a entrega da Versão 1.0.

### FASE 1: MVP Funcional (6 Meses)

| Sprint      | Meta Principal (Sprint Goal)                                    | Entregáveis Chave                                                                      |
|-------------|-----------------------------------------------------------------|----------------------------------------------------------------------------------------|
| **1-2** | Configurar o ambiente de desenvolvimento e a base de dados.       | Ambiente Docker funcional, Schema do PostGIS v1, Backlog do projeto.                   |
| **3-4** | Implementar o fluxo de autenticação e submissão de reports.    | Endpoints de auth/reports, Telas de login e submissão no app, Dados salvos no DB/Storage.  |
| **5-6** | Entregar o MVP com o fluxo de roteamento básico de ponta a ponta.  | Instância do Valhalla, Microsserviço de rota, App desenhando a rota no mapa **(MVP v1)**. |

### FASE 2: Refactoring (6 Meses)

| Sprint      | Meta Principal (Sprint Goal)                                    | Entregáveis Chave                                                                      |
|-------------|-----------------------------------------------------------------|----------------------------------------------------------------------------------------|
| **7-8** | Integrar a pipeline de IA e o monitoramento do sistema.           | Pipeline de `Image-to-Text` + `Info Extraction` funcional, Dashboard de monitoramento (Grafana). |
| **9-10** | Fazer o roteamento ser influenciado pelo `risk_score` da IA e GNN. | Modelo GNN v0 treinado, Roteamento com pesos de risco dinâmicos, Início dos testes beta. |
| **11-12** | Polir a aplicação com base no feedback e preparar o lançamento.     | App com UI/UX refinada, Documentação técnica finalizada, **Versão 1.0 do GUIA pronta.** |


-----

### Detalhamento das Sprints 

#### **Sprint 1: Fundação & Setup**

| Issue | Título | Descrição | Critérios de Aceitação | Dependências |
| :--- | :--- | :--- | :--- | :--- | 
| **\#1** | Configuração Inicial do Projeto | Configurar repositórios, board de gestão e ambiente de desenvolvimento. | - Repositórios `guia-frontend`, `guia-orchestrator`, `guia-routing-service` criados.  - Board do GitHub Projects configurado.  - `docker-compose.yml` inicial com Postgres/PostGIS. | Nenhuma |
| **\#2** | Modelagem e Migração do Banco de Dados v1 | Definir e implementar a primeira versão do schema do banco de dados. | - DBML do schema finalizado e commitado.  - Script de migração que cria as tabelas `users`, `reports`, `images`, `street_segments`, `h3_hexagons`, `ai_analyses`. | \#1 |

#### **Sprint 2: Autenticação & CI**

| Issue | Título | Descrição | Critérios de Aceitação | Dependências |
| :--- | :--- | :--- | :--- | :--- | 
| **\#3** | API de Autenticação (Backend) | Criar os endpoints para cadastro e login de usuários. | - Endpoint `POST /auth/register` funciona.  - Endpoint `POST /auth/login` retorna token JWT.  - Senhas são armazenadas com hash. | \#2 |
| **\#4** | Fluxo de Autenticação (Frontend) | Criar as telas e a lógica no app para o usuário se autenticar. | - Telas de Login e Cadastro construídas.  - Lógica para chamar as APIs de auth e gerenciar o token JWT.  - Rotas protegidas implementadas. | \#3 |
| **\#5** | Pipeline de CI Básico | Automatizar a verificação de qualidade do código a cada PR. | - GitHub Actions configurado para os repositórios.  - Etapas de *linting* e execução de testes unitários iniciais. | \#1 |

#### **Sprint 3: Ingestão de Reports**

| Issue | Título | Descrição | Critérios de Aceitação | Dependências |
| :--- | :--- | :--- | :--- | :--- | 
| **\#6** | API de Ingestão de Reports (Backend) | Desenvolver o endpoint para receber as ocorrências dos usuários. | - Endpoint `POST /reports` criado.  - Aceita coordenadas, texto e imagem.  - Salva metadados no PostGIS e faz upload da imagem para o Object Storage. | \#2 |
| **\#7** | Fluxo de Submissão de Reports (Frontend) | Criar a interface no app para o usuário enviar um report. | - Tela de submissão com acesso à câmera/GPS/texto.  - Lógica para enviar os dados para o `POST /reports`.  - O fluxo completo de login e envio é validado. | \#4, \#6 |

#### **Sprint 4: Coleta de Dados & Geohashing**

| Issue | Título | Descrição | Critérios de Aceitação | Dependências |
| :--- | :--- | :--- | :--- | :--- | 
| **\#8** | Script de Coleta de Dados (Cold Start) | Criar o script para popular o banco de dados com imagens do Street View. | - Script Python que consome a API do Street View.  - O script percorre os `street_segments` da região piloto e salva as imagens no Object Storage. | \#2 |
| **\#9** | Povoamento de Dados Geográficos | Popular o banco com a malha viária e a grade hexagonal. | - Tabela `street_segments` populada com dados do OpenStreetMap.  - Tabela `h3_hexagons` populada com a geometria dos hexágonos da região piloto. | \#2 |

#### **Sprint 5: Setup do Motor de Roteamento**

| Issue | Título | Descrição | Critérios de Aceitação | Dependências |
| :--- | :--- | :--- | :--- | :--- | 
| **\#10** | Configuração do NGINX e Fila de Tarefas | Preparar a infraestrutura de mensageria e o proxy reverso. | - Container Docker da Fila (RabbitMQ/Redis) adicionado ao `docker-compose.yml`.  - Container do NGINX configurado como proxy reverso para o Orchestrator. | \#1 |
| **\#11** | Containerização do Valhalla | Empacotar o motor de roteamento e o microsserviço em uma imagem Docker. | - Dockerfile criado para o `guia-routing-service`.  - A imagem Docker builda com sucesso, contendo Valhalla e o código do serviço. | \#10 |

#### **Sprint 6: MVP de Roteamento (Fluxo Completo)**

| Issue | Título | Descrição | Critérios de Aceitação | Dependências |
| :--- | :--- | :--- | :--- | :--- | 
| **\#12**| Lógica de Rota Assíncrona (Backend) | Orquestrar o pedido de rota usando a fila de tarefas. | - Endpoint `GET /safe-route` no Orchestrator publica uma tarefa na fila.  - Mecanismo de retorno da resposta para o cliente (WebSocket/Long Polling) implementado. | \#10 |
| **\#13**| Lógica do Microsserviço de Rota | Implementar o cálculo da rota no microsserviço. | - Serviço consome a tarefa da fila.  - Serviço chama a API do Valhalla localmente (com custo padrão).  - A polilinha da rota é publicada em uma fila de resposta. | \#11, \#12 |
| **\#14**| Roteamento no App (Frontend) | Permitir que o usuário solicite e veja a rota no mapa. | - UI para inserir origem e destino.  - Lógica para chamar a API e desenhar a rota recebida.  - **MVP é considerado funcional após esta task.** | \#12 |

#### **Sprint 7: Pipeline de IA - Image-to-Text**

| Issue | Título | Descrição | Critérios de Aceitação | Dependências |
| :--- | :--- | :--- | :--- | :--- | 
| **\#15**| Microsserviço de Image-to-Text | Criar o serviço que converte imagem em descrição textual usando Qwen. | - Serviço (ex: função serverless ou container) implementado.  - API do Qwen integrada.  - *Prompt engineering* baseado em CPTED implementado. | \#6 |
| **\#16**| Integração do Image-to-Text | Integrar o novo microsserviço no fluxo de ingestão de reports. | - Orchestrator, após salvar a imagem, chama o serviço da Issue \#15.  - A descrição textual gerada é salva na tabela `ai_analyses`. | \#15 |

#### **Sprint 8: Pipeline de IA - Extração de Risco**

| Issue | Título | Descrição | Critérios de Aceitação | Dependências |
| :--- | :--- | :--- | :--- | :--- | 
| **\#17**| Microsserviço de Extração de Fatores | Criar o serviço que extrai fatores de risco do texto usando Gemini. | - Serviço implementado.  - API do Gemini integrada.  - O serviço recebe um texto e retorna um JSON estruturado com os fatores de risco. | \#16 |
| **\#18**| Orquestração da Pipeline de IA Completa | Integrar a extração e o cálculo do `risk_score` inicial. | - Orchestrator chama o serviço da Issue \#17 após a Etapa de Image-to-Text.  - Algoritmo que converte o JSON em `risk_score` numérico é implementado.  - O `risk_score` é salvo na tabela `ai_analyses`. | \#17 |

#### **Sprint 9: Roteamento Inteligente**

| Issue | Título | Descrição | Critérios de Aceitação | Dependências |
| :--- | :--- | :--- | :--- | :--- | 
| **\#19**| Adaptação do Valhalla para Custo Dinâmico | Fazer o Valhalla usar o `risk_score` para influenciar as rotas. | - Microsserviço de roteamento consulta os `risk_scores` no PostGIS para a área da rota.  - Lógica de *dynamic costing* do Valhalla implementada para aplicar penalidades em ruas com alto risco. | \#13, \#18 |
| **\#20**| Testes de Validação do Roteamento | Garantir que as rotas estão efetivamente desviando de áreas de risco. | - Conjunto de testes A/B criado (rota normal vs. rota segura).  - Validação de que as rotas seguras geradas são diferentes e evitam os pontos de risco conhecidos. | Eng. de Software / QA | \#19 |

#### **Sprint 10: GNN - Preparação e Treinamento**

| Issue | Título | Descrição | Critérios de Aceitação | Dependências |
| :--- | :--- | :--- | :--- | :--- | 
| **\#21**| Scripts de Extração de Grafo | Preparar os dados para alimentar o modelo GNN. | - Script que extrai o grafo da cidade (nós, arestas, features) do PostGIS.  - O output é compatível com PyTorch Geometric ou DGL. | \#2, \#18 |
| **\#22**| Treinamento do Modelo GNN v0 | Treinar a primeira versão da GNN para contextualizar os `risk_scores`. | - Modelo GNN (GCN/GraphSAGE) treinado com sucesso.  - Artefatos do modelo (pesos, etc.) salvos e versionados. | \#21 |

#### **Sprint 11: GNN - Inferência e Dashboard Web**

| Issue | Título | Descrição | Critérios de Aceitação | Dependências |
| :--- | :--- | :--- | :--- | :--- | 
| **\#23**| Job de Inferência da GNN | Automatizar a atualização dos scores de risco contextualizados. | - Um job agendado (ex: Airflow, cron) executa a inferência da GNN.  - O job atualiza a coluna `gnn_risk_score` na tabela `h3_hexagons`. | \#22 |
| **\#24**| API e Dashboard Web | Criar a interface web para visualização dos mapas de calor. | - Endpoint `GET /heatmap` criado no Backend.  - Dashboard Web desenvolvido, consumindo a API e exibindo o mapa de calor da GNN. | \#23 |

#### **Sprint 12: Testes, Polimento e Documentação Final**

| Issue | Título | Descrição | Critérios de Aceitação | Dependências |
| :--- | :--- | :--- | :--- | :--- | 
| **\#25**| Testes Beta com Usuários | Coletar feedback do mundo real sobre a aplicação completa. | - Rodada de testes com um grupo de usuários selecionados é executada.  - Feedback sobre usabilidade, performance e precisão das rotas é coletado e organizado. | Gestão / Todos | \#14, \#24 |
| **\#26**| Otimização e Correção de Bugs | Refinar o produto com base no feedback e em análises de performance. | - Principais bugs reportados são corrigidos.  - Gargalos de performance identificados são otimizados.  - Build da **Versão 1.0** para o piloto é gerada. | Todos | \#25 |
| **\#27**| Finalização da Documentação | Deixar a documentação técnica completa e atualizada no MkDocs. | - Todas as seções do MkDocs (Arquitetura, Pipeline, etc.) estão preenchidas e revisadas. | Todos | \#26 |