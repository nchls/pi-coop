import React, { useEffect } from 'react';
import { useSetRecoilState } from 'recoil';


export const useAPIPoll = (atom, endpoint, pollInterval) => {
	const setter = useSetRecoilState(atom);
	useEffect(() => {
		const update = () => {
			const response = window.fetch(endpoint)
				.then((response) => response.json())
				.then((response) => {
					setter({
						fetched: true,
						...response
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