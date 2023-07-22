async function updateStreamStatus () {
  const STATUS_BASE_CLASSES = 'hero is-bold';

  const headerArea = document.getElementById('headerArea');
  const statusArea = document.getElementById('statusArea');
  statusArea.classList.add('is-hidden');

  const updatingMessageArea = document.getElementById('updatingMessage')
  updatingMessageArea.classList.remove('is-hidden');


  const response = await fetch('/status');
  const statusData = await response.json();
  let lagClass = 'is-danger';

  if (statusData.lag < 3) {
    lagClass = 'is-success';
  } else if (statusData.lag < 6) {
    lagClass = 'is-info';
  } else if (statusData.lag < 9) {
    lagClass = 'is-warning';
  } else {
    lagClass = 'is-danger';
  }

  headerArea.className = `${STATUS_BASE_CLASSES} ${lagClass}`;
  statusArea.innerHTML = `
  <div class="card m-4">
    <div class="card-content">
      <div class="media">
        <div class="media-content">
          <p class="title is-4">Consumers</p>
        </div>
      </div>
      <div class="content">
        <p class="is-size-1 has-text-centered">${statusData.consumers}</p>
      </div>
    </div>
  </div>
</div>
<div class="card m-4">
<div class="card-content">
  <div class="media">
    <div class="media-content">
      <p class="title is-4">In Progress</p>
    </div>
  </div>
  <div class="content">
    <p class="is-size-1 has-text-centered">${statusData.pending}</p>
  </div>
</div>
</div>
</div>
<div class="card m-4">
<div class="card-content">
  <div class="media">
    <div class="media-content">
      <p class="title is-4">Lag</p>
    </div>
  </div>
  <div class="content">
    <p class="is-size-1 has-text-centered">${statusData.lag}</p>
  </div>
</div>
</div>
</div>`;

  statusArea.classList.remove('is-hidden');
  updatingMessageArea.classList.add('is-hidden');
};

// Handle click on the carbon intensity button.
document.getElementById('carbonBtn').onclick = function() {
  window.location.href = '/regional/postcode/OX1';
};

// TODO handle getting the updates...
await updateStreamStatus();