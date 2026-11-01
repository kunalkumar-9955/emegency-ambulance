import 'dart:async';
import 'dart:convert';

import 'package:latlong2/latlong.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

/// WebSocket integration for driver live location (Django Channels unchanged).
class MapWebSocketService {
  WebSocketChannel? _channel;
  StreamSubscription? _subscription;
  final _driverLocationController = StreamController<DriverGpsUpdate>.broadcast();
  final _emergencyEventController = StreamController<Map<String, dynamic>>.broadcast();

  Stream<DriverGpsUpdate> get driverLocations => _driverLocationController.stream;
  Stream<Map<String, dynamic>> get emergencyEvents => _emergencyEventController.stream;

  void connectEmergency(String wsBase, String emergencyId) {
    disconnect();
    final uri = Uri.parse('$wsBase/emergency/$emergencyId/');
    _channel = WebSocketChannel.connect(uri);
    _subscription = _channel!.stream.listen(_onMessage, onError: (_) {}, onDone: disconnect);
  }

  void connectDriver(String wsBase, String driverId) {
    disconnect();
    final uri = Uri.parse('$wsBase/driver/$driverId/');
    _channel = WebSocketChannel.connect(uri);
    _subscription = _channel!.stream.listen(_onMessage, onError: (_) {}, onDone: disconnect);
  }

  void _onMessage(dynamic raw) {
    try {
      final data = jsonDecode(raw as String) as Map<String, dynamic>;
      _emergencyEventController.add(data);

      if (data['event'] == 'gps_update') {
        final lat = (data['lat'] as num?)?.toDouble();
        final lng = (data['lng'] as num?)?.toDouble();
        if (lat != null && lng != null) {
          _driverLocationController.add(DriverGpsUpdate(
            position: LatLng(lat, lng),
            etaMinutes: (data['eta_minutes'] as num?)?.toInt(),
            driverId: data['driver_id']?.toString(),
          ));
        }
      }
    } catch (_) {}
  }

  void disconnect() {
    _subscription?.cancel();
    _subscription = null;
    _channel?.sink.close();
    _channel = null;
  }

  void dispose() {
    disconnect();
    _driverLocationController.close();
    _emergencyEventController.close();
  }
}

class DriverGpsUpdate {
  final LatLng position;
  final int? etaMinutes;
  final String? driverId;

  DriverGpsUpdate({
    required this.position,
    this.etaMinutes,
    this.driverId,
  });
}
