<script lang="ts">
  import type { LatLngExpression, LatLngTuple } from "leaflet"
  import Map from "./lib/Map.svelte"
  import { onMount } from "svelte"
  import { getCity, type CityName, citiesName } from "./config/cities"
  import type { Profil } from "./config/profils"
  import type { Poi } from "./config/pois"
  import PoiCard from "./lib/PoiCard.svelte"

  let selectedCityCoordinates: LatLngTuple = [50.465803, 4.857632]
  let selectedCityName: CityName = "Namur"

  let selectedProfile: string = "nature"

  let pois: Poi[] = []
  let posPoiIds: number[] = []
  let negPoiIds: number[] = []
  let profiles: Promise<Profil[]> = Promise.resolve([])
  let radius: number = 1000

  let selectPoi: Poi | null = null
  let path: GeoJSON.Feature<GeoJSON.LineString> | null = null
  let userCoordinates: LatLngTuple = [50.465803, 4.857632]

  let isFetching = false

  function handleSelectCity(event: Event) {
    let target = event.target as HTMLSelectElement
    let name = target.value as CityName
    selectedCityName = name
    selectedCityCoordinates = getCity(name)
    userCoordinates = selectedCityCoordinates
  }

  async function getProfiles() {
    const response = await fetch(
      new URL("/profils", import.meta.env.VITE_BASE_URL_API)
    )
    return await (response.json() as Promise<Profil[]>)
  }

  function handleSelectProfil(event: Event) {
    let target = event.target as HTMLSelectElement
    let name = target.value as string
    selectedProfile = name
  }

  function handleGetPois() {
    isFetching = true
    fetch(new URL(`/nearby`, import.meta.env.VITE_BASE_URL_API), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        lat: selectedCityCoordinates[0],
        lon: selectedCityCoordinates[1],
        profil: selectedProfile,
        radius: radius,
        pos: posPoiIds,
        neg: negPoiIds,
        user: "test",
      }),
    })
      .then((response) => {
        return response.json()
      })
      .then((data) => {
        pois = data
        isFetching = false
      })
  }

  function handleGetPath(to: Poi) {
    let from: LatLngTuple = [
      selectedCityCoordinates[0],
      selectedCityCoordinates[1],
    ]
    if (selectPoi !== null) {
      from = [selectPoi.lon, selectPoi.lat]
    }
    fetch(new URL(`/path`, import.meta.env.VITE_BASE_URL_API), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        pos_from: from,
        pos_to: [to.lat, to.lon],
      }),
    })
      .then((response) => {
        return response.json()
      })
      .then((data) => {
        path = data
      })
  }

  function onPoiLike(poi: Poi) {
    posPoiIds.push(poi.id)
  }

  function onPoiDislike(poi: Poi) {
    negPoiIds.push(poi.id)
  }

  onMount(() => {
    profiles = getProfiles()
  })
</script>

<main>
  <img
    src="/quokka.png"
    style="width:5rem; aspect-ratio:1; display:inline"
    alt=""
  />
  <h1 style="display:inline; margin-left: 0.4rem">Quokka</h1>
  <label for="city" style="display:inline; margin-left: 0.4rem">
    Ville:

    <select
      style="width:15em;"
      id="city"
      bind:value={selectedCityName}
      on:change={handleSelectCity}
    >
      {#each citiesName as name}
        <option value={name}>{name}</option>
      {/each}
    </select>
  </label>

  <div class="wrapper">
    <div class="card" style="width:60vw;flex: 2;">
      <Map
        center={selectedCityCoordinates}
        user={userCoordinates}
        markers={pois.map((poi) => [poi.lat, poi.lon])}
        line={path}
        {radius}
      />
    </div>
    <div style="flex:1;height:100%;">
      <div
        style="display:flex; flex-direction:column; jutify-content:flex-start; "
      >
        <label for="profil">
          Profile:
          <select
            style="width:15em;"
            id="profil"
            bind:value={selectedProfile}
            on:change={handleSelectProfil}
          >
            {#await profiles}
              <option value="other">default</option>
            {:then profiles}
              {#each profiles as profil}
                <option value={profil.id_profil}>{profil.name}</option>
              {/each}
            {:catch error}
              <option value="other">default</option>
            {/await}
          </select>
        </label>
        <label for="radius">
          Rayon:
          <input
            style="width:15em;"
            type="range"
            id="radius"
            min="100"
            max="10000"
            step="100"
            bind:value={radius}
          />
        </label>
        {radius} m
        <button on:click={handleGetPois} aria-busy={isFetching}>
          Obtenir les POIs
        </button>
        <div style="overflow: auto;">
          {#each pois as poi}
            <PoiCard
              {poi}
              on:select={() => {
                userCoordinates = [poi.lat, poi.lon]
              }}
              on:go={() => {
                handleGetPath(poi)
              }}
              on:like={() => {
                onPoiLike(poi)
              }}
              on:dislike={() => {
                onPoiDislike(poi)
              }}
            />
          {/each}
        </div>
      </div>
    </div>
  </div>
</main>

<style>
</style>
