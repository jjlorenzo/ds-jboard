<template>
  <div class="aui-page-focused">
    <div id="page">
      <header id="header" role="banner">
        <nav class="aui-header">
          <div class="aui-header-inner">
            <div class="aui-header-primary">
              <span class="aui-header-logo aui-header-logo-textonly" />
            </div>
          </div>
        </nav>
      </header>
      <div id="content">
        <div class="aui-page-panel">
          <div class="aui-page-panel-inner" v-if="!busy">
            <section class="aui-page-panel-content" v-if="error">
              <div class="aui-message aui-message-error">
                <p class="title">
                  {{ error.name }}
                  <span class="aui-lozenge aui-lozenge-subtle aui-lozenge-error">{{ error.code }}</span>
                </p>
                <p class="title">{{ error.message }}</p>
                <small>
                  <code>{{ error.url }}</code>
                </small>
              </div>
            </section>
            <section class="aui-page-panel-content" v-if="position">
              <header class="aui-page-header">
                <div class="aui-page-header-inner">
                  <small class="aui-page-header-main">
                    <ol class="aui-nav aui-nav-breadcrumbs">
                      <li>{{ position.type }}</li>
                      <li>{{ position.location }}</li>
                      <li>{{ position.created_at.toRelative() }}</li>
                    </ol>
                    <h1>{{ position.title }}</h1>
                  </small>
                  <div class="aui-page-header-actions">
                    <div class="aui-buttons">
                      <router-link :to="{ name: 'list' }" class="aui-button aui-button-subtle">
                        <span v-if="positions">Search results</span>
                        <span v-else>Search</span>
                      </router-link>
                    </div>
                  </div>
                </div>
              </header>
              <section class="aui-page-panel-content" v-html="position.description" />
              <aside class="aui-page-panel-sidebar">
                <div class="card logo">
                  <div class="inner">
                    <h2>
                      <a target="_blank" rel="noopener" :href="position.company_url">{{ position.company }}</a>
                    </h2>
                    <img :src="position.company_logo" alt="" v-if="position.company_logo" />
                  </div>
                </div>
                <div class="card highlighted">
                  <div class="inner">
                    <h2>How to apply</h2>
                    <small v-html="position.how_to_apply"></small>
                  </div>
                </div>
              </aside>
            </section>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { FetchError } from "../errors"
import { Position } from "../store"
import { defineComponent } from "vue"
import { ref } from "vue"
import { toRef } from "vue"
import { useStore } from "../store"

export default defineComponent({
  props: {
    pk: {
      type: String,
    },
  },
  setup(props) {
    const error = ref<null | FetchError>()
    const position = ref<Position>()
    const store = useStore()
    store.dispatch("get", { pk: props.pk }).then(
      res => {
        position.value = res
      },
      err => {
        error.value = err
        console.error(err)
      },
    )
    return {
      busy: toRef(store.getters, "busy"),
      error,
      position,
      positions: toRef(store.getters, "positions"),
    }
  },
})
</script>

<style scoped>
.aui-page-header {
  border-bottom: 1px solid var(--aui-page-border);
  margin-bottom: 20px;
  padding-bottom: 20px;
}
.aui-page-panel-content > .aui-page-panel-content {
  padding: 0 20px 0 0;
}
.aui-page-panel-content > .aui-page-panel-sidebar {
  padding: 0;
}
.card {
  background-color: #efefef;
  border-radius: 5px;
  color: #777;
  margin-bottom: 10px;
  padding: 5px;
}
.card > .inner {
  background: #fafafa;
  border-radius: 5px;
  border: 1px solid #ddd;
  overflow: hidden;
  padding: 10px;
}
.card > .inner > h2 {
  border-bottom: 1px solid #ddd;
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 7px;
  padding: 0 0 5px 0;
  text-align: center;
}
.card > .inner > img {
  background-color: white;
  box-sizing: border-box;
  max-width: 100%;
  padding: 5px;
}
.card > .inner > small {
  word-break: break-all;
}
.card.highlighted {
  background-color: #edeee1;
}
.card.highlighted .inner {
  border-color: #e5e4d7;
  background-color: #fffeef;
}
.card.logo .inner {
  text-align: center;
}
</style>
