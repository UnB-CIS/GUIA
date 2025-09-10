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

### **Detalhamento das Sprints**

#### **Sprint 1: Fundação & Setup**

| Issue | Título | Descrição | Dependências |
| :--- | :--- | :--- | :--- |
| **#1** | Configuração Inicial do Projeto | Configurar repositórios, board de gestão e ambiente de desenvolvimento. | Nenhuma |
| **#2** | Modelagem e Migração do Banco de Dados v1 | Definir e implementar a primeira versão do schema do banco de dados. | #1 |

#### **Sprint 2: Autenticação & CI**

| Issue | Título | Descrição | Dependências |
| :--- | :--- | :--- | :--- |
| **#3** | API de Autenticação (Backend) | Criar os endpoints para cadastro e login de usuários. | #2 |
| **#4** | Fluxo de Autenticação (Frontend) | Criar as telas e a lógica no app para o usuário se autenticar. | #3 |
| **#5** | Pipeline de CI Básico | Automatizar a verificação de qualidade do código a cada PR. | #1 |

#### **Sprint 3: Ingestão de Reports**

| Issue | Título | Descrição | Dependências |
| :--- | :--- | :--- | :--- |
| **#6** | API de Ingestão de Reports (Backend) | Desenvolver o endpoint para receber as ocorrências dos usuários. | #2 |
| **#7** | Fluxo de Submissão de Reports (Frontend) | Criar a interface no app para o usuário enviar um report. | #4, #6 |

#### **Sprint 4: Coleta de Dados & Geohashing**

| Issue | Título | Descrição | Dependências |
| :--- | :--- | :--- | :--- |
| **#8** | Script de Coleta de Dados (Cold Start) | Criar o script para popular o banco de dados com imagens do Street View. | #2 |
| **#9** | Povoamento de Dados Geográficos | Popular o banco com a malha viária e a grade hexagonal. | #2 |

#### **Sprint 5: Setup do Motor de Roteamento**

| Issue | Título | Descrição | Dependências |
| :--- | :--- | :--- | :--- |
| **#10** | Configuração do NGINX e Fila de Tarefas | Preparar a infraestrutura de mensageria e o proxy reverso. | #1 |
| **#11** | Containerização do Valhalla | Empacotar o motor de roteamento e o microsserviço em uma imagem Docker. | #10 |

#### **Sprint 6: MVP de Roteamento (Fluxo Completo)**

| Issue | Título | Descrição | Dependências |
| :--- | :--- | :--- | :--- |
| **#12**| Lógica de Rota Assíncrona (Backend) | Orquestrar o pedido de rota usando a fila de tarefas. | #10 |
| **#13**| Lógica do Microsserviço de Rota | Implementar o cálculo da rota no microsserviço. | #11, #12 |
| **#14**| Roteamento no App (Frontend) | Permitir que o usuário solicite e veja a rota no mapa. | #12 |

#### **Sprint 7: Pipeline de IA - Image-to-Text**

| Issue | Título | Descrição | Dependências |
| :--- | :--- | :--- | :--- |
| **#15**| Microsserviço de Image-to-Text | Criar o serviço que converte imagem em descrição textual usando Qwen. | #6 |
| **#16**| Integração do Image-to-Text | Integrar o novo microsserviço no fluxo de ingestão de reports. | #15 |

#### **Sprint 8: Pipeline de IA - Extração de Risco**

| Issue | Título | Descrição | Dependências |
| :--- | :--- | :--- | :--- |
| **#17**| Microsserviço de Extração de Fatores | Criar o serviço que extrai fatores de risco do texto usando Gemini. | #16 |
| **#18**| Orquestração da Pipeline de IA Completa | Integrar a extração e o cálculo do `risk_score` inicial. | #17 |

#### **Sprint 9: Roteamento Inteligente**

| Issue | Título | Descrição | Dependências |
| :--- | :--- | :--- | :--- |
| **#19**| Adaptação do Valhalla para Custo Dinâmico | Fazer o Valhalla usar o `risk_score` para influenciar as rotas. | #13, #18 |
| **#20**| Testes de Validação do Roteamento | Garantir que as rotas estão efetivamente desviando de áreas de risco. | #19 |

#### **Sprint 10: GNN - Preparação e Treinamento**

| Issue | Título | Descrição | Dependências |
| :--- | :--- | :--- | :--- |
| **#21**| Scripts de Extração de Grafo | Preparar os dados para alimentar o modelo GNN. | #2, #18 |
| **#22**| Treinamento do Modelo GNN v0 | Treinar a primeira versão da GNN para contextualizar os `risk_scores`. | #21 |

#### **Sprint 11: GNN - Inferência e Dashboard Web**

| Issue | Título | Descrição | Dependências |
| :--- | :--- | :--- | :--- |
| **#23**| Job de Inferência da GNN | Automatizar a atualização dos scores de risco contextualizados. | #22 |
| **#24**| API e Dashboard Web | Criar a interface web para visualização dos mapas de calor. | #23 |

#### **Sprint 12: Testes, Polimento e Documentação Final**

| Issue | Título | Descrição | Dependências |
| :--- | :--- | :--- | :--- |
| **#25**| Testes Beta com Usuários | Coletar feedback do mundo real sobre a aplicação completa. | #14, #24 |
| **#26**| Otimização e Correção de Bugs | Refinar o produto com base no feedback e em análises de performance. | #25 |
| **#27**| Finalização da Documentação | Deixar a documentação técnica completa e atualizada no MkDocs. | #26 |