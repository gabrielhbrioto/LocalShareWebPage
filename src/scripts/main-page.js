let ws;

// Recupera a URL do WebSocket salva no localStorage
const wsUrl = localStorage.getItem('wsUrl');
if (!wsUrl) {
  alert('URL do WebSocket não configurada. Redirecionando para a página inicial.');
  window.location.href = '/index.html';
} else {
  console.log('Conectando ao WebSocket:', wsUrl);
  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    console.log('WebSocket conectado');
  };

  ws.onmessage = (event) => {
    console.log('Mensagem recebida da ESP32:', event.data);
    // Tratar mensagens específicas do dashboard aqui
  };

  ws.onerror = (error) => {
    console.error('Erro no WebSocket:', error);
  };

  ws.onclose = () => {
    console.log('WebSocket desconectado');
    alert('Conexão perdida com a ESP32. Redirecionando para a página de login.');
    window.location.href = './login.html';
  };
}

function toggleSection(section) {
  document.getElementById('download-section').classList.remove('active');
  document.getElementById('upload-section').classList.remove('active');
  document.getElementById(section).classList.add('active');
}

// Enviar mensagens para a ESP32 a partir do dashboard
function enviarMensagem(msg) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(msg);
    console.log('Mensagem enviada:', msg);
  } else {
    alert('Erro: WebSocket não conectado.');
  }
}