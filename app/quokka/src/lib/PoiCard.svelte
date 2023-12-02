<script lang="ts">
  import type { Poi } from "../config/pois"
  import { createEventDispatcher } from "svelte"

  export let poi: Poi

  const dispatch = createEventDispatcher()

  let isLiked = 0

  function handleLike(action: string) {
    dispatch(action)
    isLiked = action === "like" ? 1 : -1
  }
</script>

<article>
  <h5>{poi.name}</h5>
  {#if poi.image && !poi.image.startsWith("https://photos.app.goo.gl/")}
    <img src={poi.image} alt={poi.name} style="height: 5rem;" />
  {/if}
  <p>
    {poi.description ?? ""}
  </p>
  <p>
    <span>{poi.url ?? poi.website ?? ""}</span>
    <b>Cat:</b> <span>{poi.category ?? ""}</span>
    | <b>Sous cat:</b> <span>{poi.sub_category ?? ""}</span>
  </p>
  <div>
    <button on:click={() => dispatch("go")} style="display:inline;width:auto"
      >Choisir
    </button>
    <button
      on:click={() => dispatch("select")}
      style="display:inline;width:auto"
    >
      Y aller</button
    >
    <button
      disabled={isLiked !== 0}
      on:click={() => handleLike("like")}
      style="background-color:green;display:inline; width: 3rem; padding:0.4em"
    >
      👍</button
    >
    <button
      disabled={isLiked !== 0}
      on:click={() => handleLike("dislike")}
      style="margin-left:0.4em;background-color:red;display:inline; width: 3rem; padding:0.4em"
    >
      👎</button
    >
  </div>
</article>
