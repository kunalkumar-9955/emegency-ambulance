import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:geolocator/geolocator.dart';
import 'package:latlong2/latlong.dart';
import 'package:map_kit/map_kit.dart';
import '../core/config.dart';
import '../services/api_service.dart';
import '../services/offline_sync.dart';
import 'package:connectivity_plus/connectivity_plus.dart';

class EmergencyProvider extends ChangeNotifier {
  String? activeEmergencyId;
  Map<String, dynamic>? tracking;
  LatLng? patientLocation;
  LatLng? destinationLocation;
  int? etaMinutes;
  bool isLoading = false;

  final MapWebSocketService _ws = MapWebSocketService();

  Future<void> triggerSOS({String symptoms = ''}) async {
    isLoading = true;
    notifyListeners();

    final pos = await Geolocator.getCurrentPosition();
    patientLocation = LatLng(pos.latitude, pos.longitude);
    final body = {
      'pickup_latitude': pos.latitude,
      'pickup_longitude': pos.longitude,
      'symptoms': symptoms,
      'is_sos': true,
    };

    final connectivity = await Connectivity().checkConnectivity();
    if (connectivity.contains(ConnectivityResult.none)) {
      final syncId = DateTime.now().millisecondsSinceEpoch.toString();
      await OfflineSync.queueSOS(body, syncId);
      isLoading = false;
      notifyListeners();
      return;
    }

    final res = await ApiService.post('/emergencies/sos/', body);
    if (res.statusCode == 201) {
      final data = jsonDecode(res.body);
      activeEmergencyId = data['id'];
      etaMinutes = data['eta_minutes'];
      _connectTracking(activeEmergencyId!);
    }
    isLoading = false;
    notifyListeners();
  }

  void _connectTracking(String id) {
    _ws.disconnect();
    _ws.connectEmergency(AppConfig.wsBase, id);
    _ws.driverLocations.listen((update) {
      tracking = {
        'lat': update.position.latitude,
        'lng': update.position.longitude,
        'eta_minutes': update.etaMinutes,
      };
      etaMinutes = update.etaMinutes;
      notifyListeners();
    });
    _ws.emergencyEvents.listen((data) {
      tracking = data;
      if (data['eta'] != null) etaMinutes = data['eta'] as int?;
      if (data['event'] == 'gps_update') {
        final lat = (data['lat'] as num?)?.toDouble();
        final lng = (data['lng'] as num?)?.toDouble();
        if (lat != null && lng != null) {
          destinationLocation ??= LatLng(lat + 0.01, lng + 0.01);
        }
      }
      notifyListeners();
    });
  }

  @override
  void dispose() {
    _ws.dispose();
    super.dispose();
  }
}
