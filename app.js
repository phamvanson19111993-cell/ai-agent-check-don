// Render danh sách agent: số thứ tự chạy liên tục qua các nhóm, kèm icon vai trò.
(function () {
  var list = document.getElementById('agent-list');
  var index = 0;

  window.AGENT_GROUPS.forEach(function (group, gi) {
    if (gi > 0) {
      var head = document.createElement('div');
      head.className = 'group-head';
      head.innerHTML = '<span>' + group.name + '</span><button class="icon-btn" title="Thêm vào ' + group.name + '">+</button>';
      list.appendChild(head);
    }

    group.agents.forEach(function (agent) {
      index += 1;
      var row = document.createElement('button');
      row.className = 'agent-row';
      row.type = 'button';
      row.innerHTML =
        '<span class="num">' + index + '</span>' +
        '<span class="role-icon" aria-hidden="true">' + agent.icon + '</span>' +
        '<span class="text"><span class="name">' + agent.name + '</span>' +
        '<span class="role">' + agent.role + '</span></span>';
      row.addEventListener('click', function () {
        list.querySelectorAll('.agent-row.active').forEach(function (el) { el.classList.remove('active'); });
        row.classList.add('active');
      });
      list.appendChild(row);
    });
  });
})();
