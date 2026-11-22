# Gerenciador de Saúde — Projeto Final SPOLBP1

Aplicação web **MPA** (Flask + Jinja2 + sqlite3) organizada em **MVC** com Blueprints.

## Inicialização no padrão do PDF da disciplina

No Linux (Debian), na pasta do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python iniciar_bd.py
python run.py
```

No Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python iniciar_bd.py
python run.py
```

Acesse **http://127.0.0.1:5000**.

**Importante:** execute `python iniciar_bd.py` antes de `python run.py`, sobretudo em uma instalação nova. O `app/__init__.py` apenas configura o Flask, registra os Blueprints, o middleware e os handlers. O script `iniciar_bd.py` cria as tabelas com `CREATE TABLE IF NOT EXISTS` e cadastra usuários de demonstração se a tabela de usuários estiver vazia. Reexecutar o script não apaga tabelas ou registros existentes.

O arquivo SQLite fica na raiz (`banco_sistema.db`), conforme `app/db.py`. Faça cópia de segurança antes de substituir um banco já utilizado.

## Credenciais de demonstração

- João: `joao@teste.com` / `123456`
- Maria: `maria@teste.com` / `senha123`

Essas contas são apenas para demonstração acadêmica. Em hospedagem pública, remova-as ou substitua suas senhas.

## Estrutura e funcionalidades

- `iniciar_bd.py`: cria as tabelas `usuarios`, `imc_registos`, `refeicoes`, `perfil_saude` e usuários de teste.
- `run.py`: inicia o Flask.
- `app/__init__.py`: Flask, chave secreta, Blueprints, middleware e handlers 404/500.
- `app/db.py`: `DatabaseConnection` implementando `__enter__`, `__exit__`, commit, rollback, close e chaves estrangeiras.
- `app/models/`: SQL parametrizado com `?`, consultas vinculadas a `usuario_id`, POO.
- `app/controllers/`: rotas com Blueprints, validações, Flash, logs, GET/POST e chamadas aos Models, sem SQL.
- `app/utils/`: `login_required`, valida a sessão contra o banco e disponibiliza `g.usuario`.
- `app/views/`: templates HTML/Jinja2 separados: `dashboard.html`, `imc.html`, `refeicoes.html`, cadastros e edições; todos herdam de `base.html`.
- `app/static/`: CSS.

Funcionalidades: cadastro/login/logout com senhas em hash, sessões, proteção de rotas, CRUD de IMC e refeições, buscas locais por JavaScript (sem recarregar a página nem fazer registros sumirem), cookie de tema claro/escuro, mensagens Flash categorizadas, logs, validação de entradas e página 404.

A busca destaca os registros correspondentes; os demais permanecem visíveis. Ela não altera dados do SQLite. É um recurso adicional de interface, não um substituto das consultas SQL parametrizadas nos Models.

## Preparação para apresentação e entrega

Consulte `ROTEIRO_APRESENTACAO.md` para a demonstração em até 5 minutos e `MODELO_ENTREGA.txt` para preparar o documento final solicitado pelo professor. O arquivo de entrega ao Moodle é **um PDF, DOCX ou TXT com resumo, link público do GitHub e link do vídeo**; o código deve estar no repositório GitHub. Não inclua `.venv` no GitHub nem publique um banco com dados pessoais.

## Navegação MPA (sem JavaScript para trocar de tela)

As seções são páginas HTML distintas, servidas pelo Flask:

- `GET /dashboard`: visão geral (`dashboard.html`).
- `GET /imc`: formulário e histórico (`imc.html`).
- `GET /refeicoes`: formulário e lista (`refeicoes.html`).
- `GET /saude/imc/<id>/editar` e `GET /saude/refeicao/<id>/editar`: edições próprias.

A navegação utiliza links `<a href="{{ url_for(...) }}">`, e os formulários de criação, edição e exclusão usam POST. Depois de uma alteração, o Flask redireciona para o módulo correspondente (IMC ou Refeições). Não existe JavaScript para troca de página, confirmação de exclusão ou manipulação de CRUD. **O único JavaScript está no final de `imc.html` e `refeicoes.html` para destacar resultados das buscas locais**: a lista permanece visível e não é apagada do SQLite. Toda leitura e escrita de dados permanece no servidor por meio dos Models.

**Observação:** o script `iniciar_bd.py` é obrigatório no padrão da disciplina. Execute-o antes de `run.py`. O banco é preservado; faça backup antes de substituir arquivos em instalações existentes.


## Dashboard da rotina diária

Em `GET /dashboard`, o painel apresenta três informações: último IMC registrado, quantidade de refeições cadastradas **hoje** e soma das kcal cadastradas **hoje**. Mostra também uma lista das refeições de hoje com horário local, nome, descrição e kcal, em ordem cronológica. A página não contém JavaScript.

Os registros de `refeicoes.data_registro` são gravados pelo `CURRENT_TIMESTAMP` do SQLite em UTC. O Controller (`auth_controller.py`) calcula os limites do dia em `America/Sao_Paulo`, converte para UTC e chama `RefeicaoModel.buscar_por_periodo(...)` (SQL parametrizado). Nenhuma tabela precisa ser alterada ou recriada. O IMC exibido é o registro mais recente, independentemente da data.

**Limitação do cadastro:** a data da refeição corresponde ao momento do registro no sistema; não há um campo para informar uma refeição feita em um dia anterior. As kcal são informações inseridas pelo usuário e o painel apenas as soma, sem metas ou recomendações alimentares.

## Perfil pessoal, objetivo e gasto energético (nova funcionalidade)

- Execute **`python iniciar_bd.py` novamente** ao atualizar um projeto existente. O comando `CREATE TABLE IF NOT EXISTS perfil_saude` acrescenta a tabela sem apagar `usuarios`, `imc_registos` ou `refeicoes`.
- Nova página Flask: **GET/POST `/perfil`**, com template próprio `app/views/perfil.html`, sem JavaScript.
- O Model `app/models/perfil_model.py` salva um perfil por usuário, com SQL parametrizado; data de nascimento, parâmetro de sexo usado pela fórmula, atividade e objetivo de acompanhamento.
- A seleção de objetivo **não calcula dietas, restrição calórica nem ganho/perda de peso recomendado**.
- Para usuários de **12 a 17 anos**, o painel calcula uma **necessidade energética diária estimada (EER)** segundo as equações DRI/IOM para adolescentes, que levam em conta uma parcela associada ao crescimento. A partir dos **18 anos**, calcula um **gasto energético diário estimado** usando Mifflin-St Jeor e um fator aproximado de atividade. Menores de 12 anos não recebem estimativa. Ambos os números são educativos, não são metas de consumo, nem instruções para perder ou ganhar peso. O sistema exige idade, parâmetro da equação, atividade, peso e altura preenchidos.
- O painel mantém as refeições registradas hoje e a soma das kcal informadas pelo usuário; esses valores não são comparados a uma meta.
- A rota de edição usa sessão e `@login_required` para impedir que um usuário altere o perfil de outro.
- O script mantém os dados do banco atual; faça backup do seu arquivo real `banco_sistema.db` antes de substituir arquivos e **não sobrescreva o banco de produção por um banco de demonstração vindo do ZIP**.

### Cálculo de energia: limitações e referências

- **12 a 17 anos:** DRI/IOM (2006), EER para 9–18 anos, utilizando os coeficientes correspondentes aos parâmetros masculino/feminino e à atividade baixa (sedentário), moderada (ativo) ou alta (muito ativo). O resultado inclui energia associada ao crescimento; **não é somente gasto energético medido**.
- **18 anos ou mais:** Mifflin-St Jeor (adultos), multiplicado pelos fatores simplificados 1,2 / 1,55 / 1,725 conforme atividade.
- Com dados ausentes/inválidos ou idade inferior a 12 anos, a página informa que a estimativa está indisponível.
- **Aviso exibido no dashboard e no perfil:** o site é educativo e não substitui avaliação por nutricionista, médico ou outro profissional. Não há cálculo de déficit, superávit ou ingestão recomendada para objetivos de peso.
- Fonte das equações para adolescentes: *Dietary Reference Intakes for Individuals Ages 4 Through 18 Years*, tabelas K-9 e K-10, National Academies / NCBI Bookshelf: https://www.ncbi.nlm.nih.gov/books/NBK214999/ .
- Referência adicional oficial: Health Canada, *Equations to Estimate Energy Requirement*: https://www.canada.ca/en/health-canada/services/food-nutrition/food-nutrition-surveillance/health-nutrition-surveys/canadian-community-health-survey-cchs/reference-guide-understanding-using-data-2015.html .

**Nota para a apresentação:** destaque a diferença entre EER de adolescentes e GET aproximado de adultos; o site não recomenda quantidade de comida, apenas demonstra um cálculo estatístico com limitações.


## Interface moderna e personalização
- Layout responsivo com menu lateral, páginas MPA independentes e cartões informativos.
- Página `/personalizacao` com tema claro/escuro, cor principal e densidade de exibição.
- Preferências salvas em cookies (`theme`, `accent` e `density`) por Flask com `set_cookie`, lidas no template por `request.cookies`. Não requer migração do banco.
- Sem JavaScript na navegação ou personalização. O JavaScript existente permanece somente na busca local de IMC e refeições.
- Altere a aparência em **Personalização > Salvar preferências**.
