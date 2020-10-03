import React, { useEffect } from 'react';
import { useRecoilState } from 'recoil';


export const useAPIPoll = (atom, endpoint, pollInterval) => {
	const [data, setter] = useRecoilState(atom);
	useEffect(() => {
		const update = () => {
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
		update();
		const interval = setInterval(update, pollInterval);
		return () => {
			clearInterval(interval);
		};
	}, []);
};