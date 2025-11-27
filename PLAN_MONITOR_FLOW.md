# Plano de Fluxo para Monitor

## Objetivo
Criar um dashboard específico para o usuário monitor, com acesso rápido aos seus eventos, pagamentos e dados pessoais (perfil, documentos, conta bancária, uniformes, endereço/local), em uma única página com seções organizadas.

## Seções previstas (na mesma página)

### 1) Resumo rápido
- Próximo evento que ele participa  
- Total de pagamentos a receber / status (pendente/pago)  
- Contador de eventos futuros confirmados e disponibilidades ativas  

### 2) Meus eventos
- Lista dos próximos eventos onde está inscrito/convocado  
- Botão para marcar disponibilidade (se time aberto)  
- Link para detalhes do evento/time  

### 3) Pagamentos
- Últimos pagamentos (status, valor, evento)  
- Link para histórico completo (modal ou página dedicada)  

### 4) Meu perfil
- Dados básicos (nome, e-mail, categoria, códigos)  
- Ação para editar perfil  

### 5) Documentos
- Tabela/caixa com RG, CPF, PIS, CNPJ, regime  
- Ação para editar  

### 6) Conta bancária
- Banco, agência, conta, chave PIX  
- Ação para editar/criar  

### 7) Uniformes
- Tamanhos por peça  
- Ação para editar/criar  

### 8) Endereço / Local
- Endereço completo, bairro, local (cidade/estado/país) e reembolso  
- Ação para editar/criar  

---

## Regras de acesso
- Página acessível apenas para usuários autenticados com perfil de monitor.  
- Se não houver perfil vinculado, exibir um call-to-action para completar o perfil.

---

## URLs e Views (proposta)
- **URL:** `/monitor-dashboard/`  
- **View:** `monitoria.views.MonitorDashboardView` (TemplateView)  
- **Template:** `monitoria/templates/monitoria/monitor_dashboard.html`  

---

## Dados necessários (queries)
- Perfil do usuário logado + categoria  
- Disponibilidades do usuário (para saber eventos/time e status)  
- Pagamentos do usuário (filter por profile)  
- Próximo evento (availability status=True, event.start_date >= hoje)  
- Documentos, BankAccount, Uniform e Address/Location vinculados ao usuário  

---

## Próximos passos de implementação
1. Criar View/URL/Template base com layout e cartões vazios  
2. Trazer dados reais (queries por user/profile) e preencher as seções  
3. Adicionar ações (editar) com links para os formulários existentes  
4. Ajustar sidebar para perfis de monitor (opcional: condicional por role)
