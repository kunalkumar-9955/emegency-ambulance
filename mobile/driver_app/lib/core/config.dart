class DriverAppConfig {
  static const apiBase = String.fromEnvironment(
    'API_BASE',
    defaultValue: 'http://10.0.2.2:8000/api/v1',
  );
  static const wsBase = String.fromEnvironment(
    'WS_BASE',
    defaultValue: 'ws://10.0.2.2:8000/ws',
  );
}
