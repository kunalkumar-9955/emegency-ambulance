import 'package:latlong2/latlong.dart';

enum MapMarkerType { user, source, destination, ambulance, hospital, driver }

class MapMarkerData {
  final String id;
  final LatLng position;
  final MapMarkerType type;
  final String? label;
  final double? heading;

  const MapMarkerData({
    required this.id,
    required this.position,
    required this.type,
    this.label,
    this.heading,
  });

  MapMarkerData copyWith({LatLng? position, double? heading}) => MapMarkerData(
        id: id,
        position: position ?? this.position,
        type: type,
        label: label,
        heading: heading ?? this.heading,
      );
}

class RouteSegment {
  final List<LatLng> points;
  final double distanceKm;
  final int durationMinutes;
  final bool isEmergency;
  final int? trafficDelayMinutes;

  const RouteSegment({
    required this.points,
    this.distanceKm = 0,
    this.durationMinutes = 0,
    this.isEmergency = true,
    this.trafficDelayMinutes,
  });
}

class LiveTrackingState {
  final LatLng? patient;
  final LatLng? driver;
  final LatLng? destination;
  final RouteSegment? route;
  final int? etaMinutes;
  final List<MapMarkerData> nearbyAmbulances;

  const LiveTrackingState({
    this.patient,
    this.driver,
    this.destination,
    this.route,
    this.etaMinutes,
    this.nearbyAmbulances = const [],
  });

  LiveTrackingState copyWith({
    LatLng? patient,
    LatLng? driver,
    LatLng? destination,
    RouteSegment? route,
    int? etaMinutes,
    List<MapMarkerData>? nearbyAmbulances,
  }) =>
      LiveTrackingState(
        patient: patient ?? this.patient,
        driver: driver ?? this.driver,
        destination: destination ?? this.destination,
        route: route ?? this.route,
        etaMinutes: etaMinutes ?? this.etaMinutes,
        nearbyAmbulances: nearbyAmbulances ?? this.nearbyAmbulances,
      );
}
