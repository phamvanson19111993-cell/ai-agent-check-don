// Render sổ phòng: đánh số Phòng 1 → Phòng N từ trên xuống.
(function () {
  var LABEL = { wait: 'Chờ anh', ready: 'Xong, chờ duyệt', run: 'Đang chạy' };
  var list = document.getElementById('agent-list');

  window.AGENTS.forEach(function (agent, i) {
    var row = document.createElement('div');
    row.className = 'room';

    var link = '';
    if (agent.session) {
      link = '<a class="open" href="https://claude.ai/code/' + agent.session + '">Mở phòng →</a>';
    } else if (agent.doc) {
      link = '<a class="open" href="' + agent.doc + '">Xem sổ tay →</a>';
    }
    var pill = agent.status
      ? '<span class="pill ' + agent.status + '">' + LABEL[agent.status] + '</span>'
      : '<span class="pill local">💻 trên máy</span>';

    row.innerHTML =
      '<span class="rank">Phòng ' + (i + 1) + '</span>' +
      '<span class="glyph" aria-hidden="true">' + agent.icon + '</span>' +
      '<span class="body"><span class="name">' + agent.name + '</span>' +
      '<span class="role">' + agent.role + '</span></span>' +
      '<span class="meta">' + pill + link + '</span>';

    list.appendChild(row);
  });
})();
