<template>
    <header style="padding-bottom: 0rem;">
      <nav style="margin-bottom: 3rem;">
        Telegram Aircraft Bot
        <ul>
          <li><router-link to="/">TAB: Online</router-link></li>
          <li><router-link to="/telegram">Telegram Chatbot</router-link></li>
          <li><router-link to="/about">About</router-link></li>
        </ul>
      </nav>
    </header>
    <router-view />
</template>