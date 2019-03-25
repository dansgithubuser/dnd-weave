export default function get_csrf_token () {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  if (match) return match[1];
}
