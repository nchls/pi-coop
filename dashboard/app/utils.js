import React, { useEffect } from 'react';
import { useRecoilState } from 'recoil';


export const useAPIPoll = (atom, endpoint, pollInterval) => {
	const [data, setter] = useRecoilState(atom);
	let lastUpdate = 0;

	useEffect(() => {
		let interval;
		let timeout;
		
		// Hit the API and populate the atom with the result
		const update = () => {
			lastUpdate = Date.now();
			window.fetch(endpoint)
				.then((response) => {
					if (response.status > 399) {
						throw new Error(`HTTP error! status: ${response.status}`);
					}
					return response.json();
				})
				.then((response) => {
					setter({
						...data,
						...response,
						fetched: true,
						error: undefined
					});
				})
				.catch((err) => {
					console.error(err);
					setter({
						...data,
						fetched: true,
						error: err
					});
				});
		};

		// Set up the initial poll interval
		update();
		interval = setInterval(update, pollInterval);

		// When the tab loses or gains focus, clear the polling
		document.addEventListener('visibilitychange', () => {
			clearInterval(interval);
			clearTimeout(timeout);
			// And if it has gained focus, reset the polling based on the last update
			if (!document.hidden) {
				const timeToNextUpdate = pollInterval - (Date.now() - lastUpdate);
				timeout = setTimeout(() => {
					update();
					interval = setInterval(update, pollInterval);
				}, timeToNextUpdate);
			}
		});

		// On unmount, clear all intervals
		return () => {
			clearInterval(interval);
			clearTimeout(timeout);
		};
	}, []);
};