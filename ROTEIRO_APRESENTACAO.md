# Roteiro de apresentação — até 5 minutos

**0:00–0:35 | Contexto e arquitetura**  
Apresente o Gerenciador de Saúde, as entidades `usuarios`, `imc_registos` e `refeicoes`, e mostre as pastas MVC. Explique que é uma MPA com Flask, Jinja2 e sqlite3, usando Blueprints.

**0:35–1:15 | Banco de dados (critério importante)**  
Mostre `iniciar_bd.py` e explique `CREATE TABLE IF NOT EXISTS`, as duas chaves estrangeiras para `usuarios(id)` e as contas de demonstração criadas por `Usuario.salvar()`. Mostre `app/db.py`: `__enter__` abre a conexão e ativa FKs; `__exit__` usa commit/rollback e close. Mostre um Model e o SQL com `?`, vinculando operações ao `usuario_id`. Explique que é necessário executar `python iniciar_bd.py` antes de `python run.py` numa instalação nova.

**1:15–1:55 | Autenticação e segurança**  
Mostre cadastro, login com hash (sem revelar senhas internas do banco), sessão `user_id` e `username`, middleware `@login_required` com validação no SQLite e `g.usuario`. Teste uma rota protegida antes de fazer login.

**1:55–3:20 | Duas entidades — CRUD**  
Na página IMC, cadastre, liste, edite e exclua um registro. Repita na página Refeições. Explique os relacionamentos e a verificação de dono antes de editar/excluir. Use registros de demonstração, nunca dados pessoais.

**3:20–4:00 | Busca e validações**  
Demonstre a busca sem recarregar a página atual; mostre que os registros continuam visíveis e que apagar o termo restaura o destaque. Tente um formulário inválido e mostre a mensagem Flash categorizada. Explique validação feita no servidor.

**4:00–4:40 | Recursos adicionais**  
Troque o tema claro/escuro e explique `response.set_cookie` + leitura em `request.cookies`. Mostre o handler 404 e um exemplo de `app.logger` no código.

**4:40–5:00 | Entrega e justificativa**  
Mostre rapidamente README e requirements. Explique que o `iniciar_bd.py` é um script separado por exigência do padrão da aula e que a busca local em JavaScript foi adicionada como melhoria de usabilidade, preservando MVC e consultas nos Models.

> Ensaie o vídeo; não é necessário provocar erros de servidor de propósito. O professor avalia também a sua explicação e os links entregues.


## Ajuste para MPA e apresentação sem JavaScript de navegação

Abra `dashboard.html`, depois clique em **IMC** (rota `/imc`) e em **Refeições** (rota `/refeicoes`). Explique que cada clique faz um GET ao Flask, que usa `render_template` para carregar um HTML diferente, preservando a arquitetura MPA. Mostre que os botões de cadastro e edição enviam POST e retornam à seção correspondente. Explique que o JavaScript restante é **apenas um destaque visual na busca**, não manipula o banco e não faz a navegação. Mostre `iniciar_bd.py` e explique por que ele é executado antes de `run.py`.


### Demonstração adicional: painel da rotina diária

- Abra **Visão Geral**: destaque o último IMC, a quantidade de refeições de hoje e a soma de kcal do dia.
- Cadastre uma refeição em **Refeições** e volte à Visão Geral: o registro aparece na rotina de hoje e os totais mudam.
- Explique que o Controller prepara o intervalo de datas, o Model consulta o SQLite com parâmetros `?` e o Jinja2 renderiza o HTML; não há JavaScript nessa página.
- O `iniciar_bd.py` continua separado para atender à estrutura do trabalho.


### Perfil e gasto energético (nova tela MPA)
Mostre a página **Meu Perfil** (`/perfil`), salve uma preferência de acompanhamento e explique a tabela `perfil_saude` relacionada a `usuarios` por chave estrangeira `usuario_id UNIQUE`. Volte ao dashboard e mostre o objetivo persistido. Explique que o programa usa peso e altura do último IMC e apresenta estimativa educativa de necessidade energética para usuários de 12 a 17 anos (equações DRI/IOM com crescimento) e de gasto energético para adultos (Mifflin-St Jeor). Reforce que o valor é aproximado e não substitui nutricionista ou médico; não há metas alimentares automáticas. O formulário é um POST Flask comum, sem JavaScript. Ao atualizar projeto existente, execute de novo `python iniciar_bd.py` para criar a nova tabela sem apagar registros.
