<script lang="ts">
  import "leaflet/dist/leaflet.css"
  import "leaflet"
  import L, { type LatLngExpression, type LatLngTuple } from "leaflet"
  import quokkaImg from "../assets/quokka.png"
  import type { Poi } from "../config/pois"
  import { createEventDispatcher } from "svelte"

  export let center: LatLngExpression = [50.465803, 4.857632]
  export let line: GeoJSON.Feature<GeoJSON.LineString> | null = null
  export let markers: LatLngExpression[] = []
  export let pois: Poi[] = []
  export let user: LatLngExpression = [50.465803, 4.857632]
  export let radius: number = 1000

  let markerLayers: L.LayerGroup | null = null
  let poisLayers: L.LayerGroup | null = null
  let lineLayers: L.Polyline | null = null
  let circleLayers: L.Circle | null = null

  let map: L.Map | null = null

  let centerMarker: L.Marker | null = null

  const initialView: LatLngTuple = [50.465803, 4.857632]
  const dispatch = createEventDispatcher()

  $: if (center && map) {
    setCenter(center)
  }
  $: if (user && map) {
    updateCenterMarker(user)
  }

  $: if (line && map) {
    updateLine(line)
  }

  $: if (markers && map) {
    if (markerLayers) {
      markerLayers.remove()
    }
    markerLayers = L.layerGroup()
    for (let location of markers) {
      let m = createMarker(location)
      markerLayers.addLayer(m)
    }
    markerLayers.addTo(map)
  }

  $: if (pois && map) {
    for (const poi of pois) {
      createPoi(poi)
    }
  }

  $: if (radius && map && user && centerMarker) {
    updateCircle(user, radius)
  }

  function updateCircle(center: LatLngExpression, radius: number) {
    if (circleLayers) {
      circleLayers.setLatLng(center)
      circleLayers.setRadius(radius)
    } else if (map) {
      circleLayers = L.circle(center, {
        color: "#E4E",
        opacity: 0.6,
        radius: radius,
        weight: 1,
        stroke: true,
        fillOpacity: 0.05,
      }).addTo(map)
    }
  }

  function updateCenterMarker(center: LatLngExpression) {
    if (centerMarker) {
      centerMarker.setLatLng(center)
      map!.panTo(center)
    } else if (map) {
      centerMarker = L.marker(center, {
        icon: new L.Icon({ iconUrl: quokkaImg, iconSize: [24, 24] }),
      }).addTo(map)
      centerMarker.setZIndexOffset(1000)
    }
  }

  function updateLine(line: GeoJSON.Feature<GeoJSON.LineString>) {
    if (lineLayers) {
      lineLayers.remove()
    }
    lineLayers = createLines(line)
    if (lineLayers && map) {
      lineLayers.addTo(map)
    }
  }

  function createMap(container: HTMLElement) {
    let m = L.map(container).setView(initialView, 14)
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution:
        'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
      maxZoom: 18,
    }).addTo(m)

    poisLayers = L.layerGroup(undefined)
    poisLayers.addTo(m)

    return m
  }

  function createMarker(loc: LatLngExpression) {
    let marker = L.marker(loc)

    return marker
  }

  function createPoi(poi: Poi) {
    if (poisLayers) {
      const m = createMarker([poi.lat, poi.lon])
      m.bindPopup(`<span>${poi.name}</span>`)
      m.addEventListener("click", () => {
        dispatch("select", poi)
      })
      poisLayers.addLayer(m)
    }
  }

  function createLines(line: GeoJSON.Feature<GeoJSON.LineString>) {
    if (!line) {
      return null
    }
    return L.polyline(line.geometry.coordinates as LatLngExpression[], {
      color: "#97d4e4",
      opacity: 1,
      stroke: true,
      weight: 6,
    })
  }

  function mapAction(container: HTMLElement) {
    map = createMap(container)

    markerLayers = L.layerGroup()
    for (let location of markers) {
      let m = createMarker(location)
      markerLayers.addLayer(m)
    }
    if (line) {
      lineLayers = createLines(line)
      if (lineLayers) {
        lineLayers.addTo(map)
      }
    }

    markerLayers.addTo(map)

    return {
      destroy: () => {
        map?.remove()
        map = null
      },
    }
  }

  function resizeMap() {
    if (map) {
      map.invalidateSize()
    }
  }

  function setCenter(center: LatLngExpression) {
    if (map) {
      map.setView(center, 15)
    }
  }
</script>

<svelte:window on:resize={resizeMap} />

<div id="map" style="height: 100%; weigth:100%" use:mapAction></div>
