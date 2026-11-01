import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_map/flutter_map.dart' as fm;
import 'package:latlong2/latlong.dart';

import '../models/map_models.dart';
import '../services/map_service.dart';
import '../services/osm_tile_cache.dart';

/// Reusable map state: markers, theme, zoom, nearby ambulances.
class EmergencyMapController extends ChangeNotifier {
  EmergencyMapController(this._mapService);

  final MapService _mapService;

  final fm.MapController mapController = fm.MapController();
  bool darkMode = false;
  bool isLoading = true;
  LatLng? userLocation;
  final List<MapMarkerData> markers = [];
  RouteSegment? activeRoute;

  StreamSubscription<LatLng>? _locationSub;

  Future<void> initialize() async {
    isLoading = true;
    notifyListeners();

    userLocation = await _mapService.currentUserLocation();
    if (userLocation != null) {
      await _mapService.prefetchOfflineArea(userLocation!);
      final nearby = await _mapService.fetchNearbyAmbulances(userLocation!);
      markers.removeWhere((m) => m.type == MapMarkerType.ambulance || m.type == MapMarkerType.hospital);
      markers.addAll(nearby);
      _setUserMarker(userLocation!);
      mapController.move(userLocation!, 14);
    }

    _locationSub?.cancel();
    _locationSub = _mapService.location.watchPosition(distanceFilterMeters: 20).listen((pos) {
      userLocation = pos;
      _setUserMarker(pos);
      notifyListeners();
    });

    isLoading = false;
    notifyListeners();
  }

  void _setUserMarker(LatLng pos) {
    markers.removeWhere((m) => m.type == MapMarkerType.user);
    markers.add(MapMarkerData(id: 'user', position: pos, type: MapMarkerType.user, label: 'You'));
  }

  void setSourceDestination({
    required LatLng source,
    required LatLng destination,
  }) {
    markers.removeWhere((m) => m.type == MapMarkerType.source || m.type == MapMarkerType.destination);
    markers.add(MapMarkerData(id: 'source', position: source, type: MapMarkerType.source, label: 'Pickup'));
    markers.add(MapMarkerData(
      id: 'destination',
      position: destination,
      type: MapMarkerType.destination,
      label: 'Hospital',
    ));
    notifyListeners();
  }

  Future<void> drawRoute(LatLng from, LatLng to, {LatLng? driver}) async {
    activeRoute = await _mapService.buildEmergencyRoute(
      source: from,
      destination: to,
      driver: driver,
    );
    notifyListeners();
    if (activeRoute != null && activeRoute!.points.isNotEmpty) {
      mapController.fitCamera(
        fm.CameraFit.coordinates(
          coordinates: activeRoute!.points,
          padding: const EdgeInsets.all(48),
        ),
      );
    }
  }

  void addAmbulanceMarker(String id, LatLng pos, {String? label}) {
    markers.removeWhere((m) => m.id == id);
    markers.add(MapMarkerData(id: id, position: pos, type: MapMarkerType.ambulance, label: label));
    notifyListeners();
  }

  void toggleDarkMode() {
    darkMode = !darkMode;
    notifyListeners();
  }

  void zoomIn() => mapController.move(
        mapController.camera.center,
        mapController.camera.zoom + 1,
      );

  void zoomOut() => mapController.move(
        mapController.camera.center,
        mapController.camera.zoom - 1,
      );

  void centerOnUser() {
    if (userLocation != null) {
      mapController.move(userLocation!, 15);
    }
  }

  fm.TileLayer get tileLayer => OsmTileCache.buildTileLayer(darkMode: darkMode);

  @override
  void dispose() {
    _locationSub?.cancel();
    _mapService.location.dispose();
    super.dispose();
  }
}
