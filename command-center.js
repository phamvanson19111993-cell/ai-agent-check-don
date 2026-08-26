// Render trang Command Center từ departments.js.
(function () {
  var esc = function (s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); };

  // 5 trường bắt buộc của một dữ liệu
  ['Giá trị', 'Nguồn', 'Kỳ dữ liệu', 'Trạng thái xác minh', 'Phòng cung cấp'].forEach(function (f, i) {
    var chip = document.createElement('span');
    chip.className = 'chip';
    chip.innerHTML = '<span class="chip-n">' + (i + 1) + '</span>' + esc(f);
    document.getElementById('fields').appendChild(chip);
  });

  var list = document.getElementById('dept-list');
  window.DEPARTMENTS.forEach(function (d, i) {
    var row = document.createElement('div');
    row.className = 'room dept';

    var owns = d.owns.map(function (o) { return '<span class="tag">' + esc(o) + '</span>'; }).join('');
    var rule = d.rule ? '<span class="rule">⛔ ' + esc(d.rule) + '</span>' : '';
    var feeds = d.feeds.length
      ? '<span class="feeds">Agent đang bơm dữ liệu: ' + d.feeds.map(esc).join(' · ') + '</span>'
      : '<span class="feeds gap">⚠️ Chưa có agent phụ trách — dữ liệu phòng này phải hỏi anh</span>';

    row.innerHTML =
      '<span class="rank">Phòng ' + (i + 1) + '</span>' +
      '<span class="glyph" aria-hidden="true">' + d.icon + '</span>' +
      '<span class="body"><span class="name">' + esc(d.name) + '</span>' +
      '<span class="role">' + esc(d.role) + '</span>' +
      '<span class="tags">' + owns + '</span>' + rule + feeds + '</span>';

    list.appendChild(row);
  });

  var steps = document.getElementById('step-list');
  window.STEPS.forEach(function (s) {
    var row = document.createElement('div');
    row.className = 'room step';
    row.innerHTML =
      '<span class="rank">Bước ' + s.n + '</span>' +
      '<span class="body"><span class="name">' + esc(s.name) + '</span>' +
      '<span class="role">' + esc(s.note) + '</span></span>';
    steps.appendChild(row);
  });

  var pri = document.getElementById('priority');
  window.PRIORITY.forEach(function (p) {
    var li = document.createElement('li');
    li.textContent = p;
    pri.appendChild(li);
  });
})();
