<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

import jsonData from '../test.json'

import { type FlightRequest, type AircraftDescriptionRequest, type FlightObservation, getFlights, getAircraftInformation } from "../api/api";
import FlightObservationCard from '../components/FlightObservationCard.vue'
import LoadingMessage from '../components/LoadingMessage.vue';
import ErrorCard from '../components/ErrorCard.vue'

enum PageState {
    NoRequestYet,
    HandlingRequest,
    ResultsReady
}

type ErrorDisplay = {
    message: string
    id: string
}

const errors = ref<ErrorDisplay[]>([])
const createError = (message: string): ErrorDisplay => ({ message, id: crypto.randomUUID() })
const clearErrors = () => errors.value = []
const addError = (error: ErrorDisplay) => errors.value.push(error)
const removeError = (id: string) => errors.value = errors.value.filter(e => e.id != id)

const userPosition = ref({ latitude: 0, longitude: 0 })

const state = ref(PageState.NoRequestYet);

const flights = ref<FlightObservation[]>()
const radar_bytes = ref<string>()

function getPosition(options?: PositionOptions): Promise<GeolocationPosition> {
    return new Promise((resolve, reject) =>
        navigator.geolocation.getCurrentPosition(resolve, reject, options)
    );
}

const handleClick = async () => {
    try {
        clearErrors()
        state.value = PageState.HandlingRequest

        const position = await getPosition();
        userPosition.value = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
        }

        let flightRequest = userPosition.value
        let response = await getFlights(flightRequest)
        flights.value = response.observations
        radar_bytes.value = response.radar_map

        state.value = PageState.ResultsReady

    } catch (err: any) {
        if (err.code == 1) {
            addError(createError("Please allow location permissions for this website. Refresh the page or allow location access."))
        } else if (err.message.includes("Failed to fetch flights")) {
            addError(createError("Server error: cannot connect to API. Please try again later."))
        } else {
            addError(createError("Unhandled error, please try again later."))
        }

        console.error({ err });
        state.value = PageState.NoRequestYet
    }
}

const radar_url = computed(() => "data:image/png;base64," + radar_bytes.value)

const loadingMessages = ["Cloudy with a chance of planes",
    "Aircraft inbound", "Loading sky magic", "No turbulence, just patience", "Aircraft, on their way"];

const getRandomLoadingMessage = () => {
    const randomIndex = Math.floor(Math.random() * loadingMessages.length);
    return loadingMessages[randomIndex];
}

function convert_bearing_to_eight_point_cardinal(bearing: number) {
    // Ensure the bearing is within the range [0, 360)
    bearing = (bearing % 360 + 360) % 360;

    // Define cardinal directions and corresponding ranges
    const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
    const ranges = [22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5];

    for (let i = 0; i < directions.length; i++) {
        if (bearing < ranges[i]) {
            return directions[i];
        }
    }
    return 'N';
}
</script>

<template>
    <h1>Send me your location, find nearby aircraft</h1>
    <p>For the best experience, use the <a>Telegram chatbot</a> (much faster than website)</p>

    <p>
        <template v-if="state != PageState.ResultsReady">
            <button @click="handleClick">Find flights near me!</button>
        </template>
        <template v-else>
            <button @click="handleClick" style="margin-right: 5px;">Repeat search &#128257;</button>

            <router-link to="/telegram" tag="span">
                <button @click="handleClick" style="margin-left: 5px;">Learn about the Telegram bot</button>
            </router-link>
        </template>
    </p>

    <section v-if="state == PageState.HandlingRequest">
        <aside>
            <LoadingMessage :count="3" :interval="500" :message="getRandomLoadingMessage()" :symbol="`.`"></LoadingMessage>
        </aside>
    </section>

    <section v-if="errors.length > 0">
        <ErrorCard v-for="error in errors" :key="error.id" :message="error.message" :id="error.id"
            @alert-dismissed="() => removeError(error.id)"></ErrorCard>
    </section>

    <template v-if="state == PageState.ResultsReady">

        <section id="radar">
            <aside style="width: auto">
                <img v-if="radar_bytes" :src="radar_url" width="800" height="800">
            </aside>
        </section>

        <section id="section-1">
            <aside v-for="flight in flights" :key="flight.callsign">
                <h3>{{ flight.callsign }}</h3>
                <h2>{{ flight.aircraft }}</h2>
                <img v-if="flight.photo" :src="flight.photo" />
                <p>
                    <strong>Origin:</strong> {{ flight.origin }}<br>
                    <strong>Destination:</strong> {{ flight.destination }}<br>
                    <strong>Flying:</strong> {{ convert_bearing_to_eight_point_cardinal(flight.heading) }}<br>
                    <strong>Look:</strong> {{ convert_bearing_to_eight_point_cardinal(flight.relative_angle) }}<br>
                    <strong>Distance:</strong> {{ Math.round(flight.ground_distance) }}km
                </p>
            </aside>
        </section>

    </template>
</template>
