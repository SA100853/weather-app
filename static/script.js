document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('toggleTheme');
  const body = document.body;

  // Load theme from local storage
  if (localStorage.getItem('theme') === 'dark') {
    body.classList.remove('light');
    body.classList.add('dark');
  }

  toggle.addEventListener('click', () => {
    body.classList.toggle('dark');
    body.classList.toggle('light');
    localStorage.setItem('theme', body.classList.contains('dark') ? 'dark' : 'light');
  });
});
